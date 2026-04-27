"""new command/script."""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from christianwhocodes import (
    BaseCommand,
    ExitCode,
    Text,
    cprint,
    status,
)

from ...conf import (
    API_NAME,
    API_VERSION,
    PROJECT_API,
    DatabaseHelpTexts,
    DatabaseKeys,
    DatabaseOptions,
    LayoutDefaults,
    LayoutHelpTexts,
    LayoutKeys,
    LayoutOptions,
    PresetDefaults,
    PresetHelpTexts,
    PresetKeys,
    PresetOptions,
)

__all__ = ["NewCommand"]


class NewCommand(BaseCommand):
    """Command to initialize a new project."""

    _project_dir: Path
    _validated_args: Namespace
    _project_dir_existed_before: bool
    prog = API_NAME + " new"
    help = f"Initialize a new {PROJECT_API.base_display_name} app."

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Register arguments onto the parser."""
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=API_VERSION,
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
            f"--{LayoutKeys.LAYOUT.value}",
            choices=list(LayoutOptions),
            default=LayoutDefaults.OPTION.value,
            help=LayoutHelpTexts.OPTION.value,
        )

        parser.add_argument(
            f"--{LayoutKeys.DASHBOARD.value}",
            default=LayoutDefaults.DASHBOARD.value,
            help=LayoutHelpTexts.DASHBOARD.value,
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
        """Create the dashboard folder and necessary files using Django's startapp."""
        from django.core.management import call_command

        dashboard_name = getattr(args, LayoutKeys.DASHBOARD)
        dashboard_dir: Path = project_dir / dashboard_name
        dashboard_dir.mkdir(parents=True, exist_ok=True)

        call_command("startapp", dashboard_name, str(dashboard_dir))

        # Rename the AppConfig base class definition to avoid naming conflicts.
        # Only needed when using the default dashboard name, as custom names will have
        # unique AppConfig class names generated by Django's startapp command.
        if dashboard_name == LayoutDefaults.DASHBOARD.value:
            apps_py_path = dashboard_dir / "apps.py"
            if apps_py_path.exists():
                apps_py_content = apps_py_path.read_text(encoding="utf-8")
                apps_py_content = apps_py_content.replace(
                    "class AppConfig(AppConfig):",
                    "class DashboardConfig(AppConfig):",
                )
                apps_py_path.write_text(apps_py_content, encoding="utf-8")

        # Overwrite urls.py, views.py, and create the layout file
        views_content = (
            "from django.views.generic.base import TemplateView\n\n\n"
            "class HomeView(TemplateView):\n"
            f'    template_name = "{dashboard_name}/layout.html"\n'
        )
        (dashboard_dir / "views.py").write_text(views_content, encoding="utf-8")

        urls_content = (
            "from django.urls import path\n\n"
            "from . import views\n\n"
            "urlpatterns = [\n"
            f'    path("", views.HomeView.as_view(), name="home"),\n'
            "]\n"
        )
        (dashboard_dir / "urls.py").write_text(urls_content, encoding="utf-8")

        layout_html_content = (
            '{% extends "base/layout.html" %}\n'
            "{% block sections %}\n"
            '    <section class="container">\n'
            '        <p class="text-primary">Welcome to our App!</p>\n'
            "    </section>\n"
            "{% endblock sections %}\n"
        )
        templates_dir = dashboard_dir / "templates" / dashboard_name
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
        setattr(
            generate_args, LayoutKeys.DASHBOARD, getattr(args, LayoutKeys.DASHBOARD)
        )

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
            f"✓ {PROJECT_API.base_display_name} project '{project_dir.name}' initialized successfully!",
            Text.SUCCESS,
        )
