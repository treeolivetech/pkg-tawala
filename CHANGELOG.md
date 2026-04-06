## v1.4.1
- When initializaing a new project with vercel preset, the .gitignore now includes igorreing the `.vercel` folder.
- Renamed `PresetOptions` enum to `ProjectPresetOptions`, and `PresetFlags` to `ProjectPresetFlags` 
- Updated enumerations for Storage backend options to match project preset options. Note that The Storage backend option `default` means that the default django file system storage backend is used while `vercel` means we're using Vercel Blob storage.
