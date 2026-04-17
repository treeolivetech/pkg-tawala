"""`newproject` command/script."""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from christianwhocodes import (
    BaseCommand,
    ExitCode,
    Text,
    cprint,
    status,
)

from tawala import (
    FETCH_PROJECT,
    DatabaseHelpTexts,
    DatabaseKeys,
    DatabaseOptions,
    LayoutKeys,
    LayoutOptions,
    PresetHelpTexts,
    PresetKeys,
    PresetOptions,
    PresetDefaults,
)

from .. import PKG_NAME, PKG_VERSION

__all__ = ["NewCommand"]


class NewCommand(BaseCommand):
    """Command to initialize a new project."""

    _project_dir: Path
    _validated_args: Namespace
    _project_dir_existed_before: bool
    prog = PKG_NAME + " new"
    help = f"Initialize a new {FETCH_PROJECT.pkg_display_name} app."

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Register arguments onto the parser."""
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=PKG_VERSION,
            help="Show package version and exit.",
        )

        parser.add_argument(
            "-p",
            "--project",
            dest="project_name",
            required=True,
            help=(
                "Name of the project to initialize. Can also be '.' to initialize in the current directory."
            ),
        )

        parser.add_argument(
            f"--{PresetKeys.PRESET.value}",
            choices=list(PresetOptions),
            default=PresetDefaults.OPTION.value,
            help=PresetHelpTexts.OPTION.value,
        )

        parser.add_argument(
            f"--{DatabaseKeys.DB.value}",
            choices=list(DatabaseOptions),
            help=DatabaseHelpTexts.OPTION.value,
        )

        parser.add_argument(
            f"--{DatabaseKeys.USE_VARS_OPTION.value}",
            action="store_true",
            help=DatabaseHelpTexts.USE_VARS_OPTION.value,
        )

        parser.add_argument(
            f"--{LayoutKeys.LAYOUT}",
            choices=list(LayoutOptions),
            help=f"Layout to use for the generated project. Defaults to the standard {LayoutOptions.BASE} layout if not specified.",
        )

    def handle(self, args: Namespace) -> ExitCode:
        """Execute the command logic with the parsed arguments."""
        try:
            self._project_dir = Path.cwd() / args.project_name
            self._project_dir_existed_before = self._project_dir.exists()
            self._validated_args = self._validate_args(args)
            self._validate_project_directory(self._project_dir, self._validated_args)
            with status("Generating project files..."):
                self._run_generate_command(
                    "all", self._project_dir, self._validated_args
                )
            with status("Generating app..."):
                self._run_startapp_command(self._project_dir, self._validated_args)
        except Exception as e:
            cprint(
                f"Something went wrong during project initialization:\n{e}",
                Text.WARNING,
            )
            self._revert_generated_files(self._project_dir)
            return ExitCode.ERROR
        else:
            self._display_successful_setup_info(self._project_dir)
            return ExitCode.SUCCESS

    def _validate_args(self, args: Namespace) -> Namespace:
        match getattr(args, PresetKeys.PRESET):
            case PresetOptions.VERCEL:
                # Enforce postgresql and environment variable configuration for Vercel preset
                # due to platform requirements and security best practices.
                if getattr(args, DatabaseKeys.DB) == DatabaseOptions.SQLITE:
                    raise ValueError(
                        f"The {PresetOptions.VERCEL} preset requires {DatabaseOptions.POSTGRESQL}."
                    )
                setattr(args, DatabaseKeys.DB, DatabaseOptions.POSTGRESQL)
                setattr(args, DatabaseKeys.USE_VARS_OPTION, True)
            case _:
                # Other presets work with either database.
                # Default to sqlite if getattr(args, DatabaseKeys.DB) is unspecified.
                if not getattr(args, DatabaseKeys.DB):
                    setattr(
                        args,
                        DatabaseKeys.DB,
                        DatabaseOptions.SQLITE,
                    )

        if (
            getattr(args, DatabaseKeys.USE_VARS_OPTION)
            and not getattr(args, DatabaseKeys.DB) == DatabaseOptions.POSTGRESQL
        ):
            raise ValueError(
                f"The --{DatabaseKeys.USE_VARS_OPTION} flag is only supported for {DatabaseOptions.POSTGRESQL}."
            )

        return args

    def _validate_project_directory(self, project_dir: Path, args: Namespace) -> None:
        """Ensure destination directory is safe to initialize."""
        if args.project_name == "." and any(project_dir.iterdir()):
            raise FileExistsError(
                "The current directory is not empty. "
                "Please choose a different project name or remove the existing files."
            )
        if not project_dir.exists():
            return
        if project_dir.is_file():
            raise FileExistsError(
                f"A file named '{project_dir}' already exists. "
                "Please choose a different project name or remove the existing file."
            )
        if any(project_dir.iterdir()):
            raise FileExistsError(
                f"The directory '{project_dir}' already exists and is not empty. "
                "Please choose a different project name or remove the existing files "
                "in the directory."
            )

    def _run_startapp_command(self, project_dir: Path, args: Namespace) -> None:
        """Create the app folder and necessary files using Django's startapp."""
        from django.core.management import call_command

        app_name = "app"
        app_dir = project_dir / app_name
        app_dir.mkdir(parents=True, exist_ok=True)

        call_command("startapp", app_name, str(app_dir))

        # Rename the AppConfig base class definition to avoid naming conflicts
        apps_py_path = app_dir / "apps.py"
        if apps_py_path.exists():
            apps_py_content = apps_py_path.read_text(encoding="utf-8")
            apps_py_content = apps_py_content.replace(
                "from django.apps import AppConfig",
                "from django.apps import AppConfig as DjangoAppConfig",
            ).replace(
                "class AppConfig(AppConfig):",
                "class AppConfig(DjangoAppConfig):",
            )
            apps_py_path.write_text(apps_py_content, encoding="utf-8")

        # Overwrite urls.py, views.py, and create the layout file
        views_content = (
            "from django.views.generic.base import TemplateView\n\n\n"
            "class HomeView(TemplateView):\n"
            f'    template_name = "{app_name}/layout.html"\n'
        )
        (app_dir / "views.py").write_text(views_content, encoding="utf-8")

        urls_content = (
            f'"""URL configuration for {project_dir.name} project.\n\n'
            "The `urlpatterns` list routes URLs to views. For more information please see:\n"
            "    https://docs.djangoproject.com/en/stable/topics/http/urls/\n"
            '"""\n\n'
            "from django.urls import path\n\n"
            "from . import views\n\n"
            "urlpatterns = [\n"
            f'    path("", views.HomeView.as_view(), name="home"),\n'
            "]\n"
        )
        (app_dir / "urls.py").write_text(urls_content, encoding="utf-8")

        layout_html_content = (
            '{% extends "base/layout.html" %}\n'
            "{% block fonts %}\n"
            '    <link href="https://fonts.googleapis.com" rel="preconnect" />\n'
            '    <link href="https://fonts.gstatic.com" rel="preconnect" crossorigin />\n'
            '    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&family=Raleway:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Mulish:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap"\n'
            '          rel="stylesheet" />\n'
            "{% endblock fonts %}\n"
            "{% block main %}\n"
            "    <main>\n"
            '        <section class="container">\n'
            '            <p class="text-primary">Welcome to our App!</p>\n'
            "        </section>\n"
            "    </main>\n"
            "{% endblock main %}\n"
        )
        templates_dir = app_dir / "templates" / app_name
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "layout.html").write_text(
            layout_html_content, encoding="utf-8"
        )

    def _run_generate_command(
        self,
        target: str,
        project_dir: Path,
        args: Namespace,
    ) -> None:
        """Invoke the generate subcommand directly for decoupled scaffolding."""
        from .generate import GenerateCommand

        generate_args = Namespace(
            target=target,
            output_dir=str(project_dir),
            project_name=project_dir.name,
        )
        setattr(generate_args, PresetKeys.PRESET, getattr(args, PresetKeys.PRESET))
        setattr(generate_args, DatabaseKeys.DB, getattr(args, DatabaseKeys.DB))
        setattr(
            generate_args,
            DatabaseKeys.USE_VARS_OPTION,
            getattr(args, DatabaseKeys.USE_VARS_OPTION),
        )
        setattr(generate_args, LayoutKeys.LAYOUT, getattr(args, LayoutKeys.LAYOUT))

        generate_command = GenerateCommand()
        exit_code = generate_command.handle(generate_args)

        if exit_code != ExitCode.SUCCESS:
            raise RuntimeError(f"Generate command failed for target '{target}'")

    def _revert_generated_files(self, project_dir: Path) -> None:
        """Delete generated files only when the target directory was newly created."""
        # Never clean up pre-existing directories to avoid deleting user files
        # (especially when the user attempted initialization in '.').
        if self._project_dir_existed_before:
            return

        if project_dir.exists() and project_dir.is_dir() and any(project_dir.iterdir()):
            for item in sorted(project_dir.rglob("*"), reverse=True):
                item.unlink() if item.is_file() else item.rmdir()

    def _display_successful_setup_info(self, project_dir: Path) -> None:
        """Print success output after initialization."""
        cprint(
            f"✓ {FETCH_PROJECT.pkg_display_name} project '{project_dir.name}' initialized successfully!",
            Text.SUCCESS,
        )
