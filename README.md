# Lumen RT — Runtime Dependencies

This repository hosts third-party runtime components used by **Lumen RT**, a Minecraft Java Edition Vulkan-based ray tracing mod.

## Slang Compiler — Windows and Linux x64

The current release provides the **unmodified Slang v2026.21** command-line compilers from the official [Slang project](https://github.com/shader-slang/slang/releases/tag/v2026.21), the latest stable upstream release verified on November 9, 2026.

Lumen RT uses Slang to compile shaders at runtime, including shaders for custom rendering effects from other mods. The compiler is optional for the mod's core ray tracing features; some custom effects require a successful runtime compilation.

On supported systems, Lumen RT automatically downloads the matching executable in the background when Minecraft starts, unless a verified copy is already cached. Downloads use HTTPS and are checked against the expected file size and SHA-256 before execution. Linux executable permission is set automatically. **Manual installation is normally not required.**

### Downloads

| Platform | Executable | Requirements |
| --- | --- | --- |
| Windows x64 | [slangc.exe v2026.21](https://github.com/rmiss1/lumenrt-dependencies/releases/download/slangc-v2026.21/slangc.exe) | Matching v2026.21 compiler DLLs, bundled with Lumen RT |
| Linux x64 | [slangc-linux-x64 v2026.21](https://github.com/rmiss1/lumenrt-dependencies/releases/download/slangc-v2026.21/slangc-linux-x64) | glibc 2.27 or newer and matching v2026.21 compiler shared libraries, bundled with Lumen RT |

Linux uses a native ELF executable, installed locally as `slangc`; a Windows `.exe` cannot run natively on Linux. These executables are **not standalone distributions** and must be used with the matching libraries. The mod JAR contains the DLL/SO libraries and their notices, while both compiler executables are downloaded from this release.

- [Release details](https://github.com/rmiss1/lumenrt-dependencies/releases/tag/slangc-v2026.21)
- [SHA-256 inventory](https://github.com/rmiss1/lumenrt-dependencies/releases/download/slangc-v2026.21/files.sha256)
- Windows `slangc.exe` (295,936 bytes): `71d56bcc90709700b318413bfced07a4b7378c76b2bbc539e89f2d2c90b1e5f8`
- Linux `slangc-linux-x64` (227,984 bytes): `769db0bbee754f4f534f725055c74da113f9cc36857c86e581f6fb52a62c30aa`

Compiler files and libraries are cached separately by operating system and compiler version. Linked shader caches include the matching compiler inventory, so an older compiler's cached output is not reused after an update. No Vulkan SDK or system-wide Slang installation is required for runtime compilation. This Lumen RT distribution supports x86_64/amd64 on Windows and Linux; macOS and ARM64 are not included.

### Archived release

[Windows Slang v2026.8](https://github.com/rmiss1/lumenrt-dependencies/releases/tag/slangc-windows-x64-v2026.8) is retained for older Lumen RT builds that reference its fixed download URL. New builds use v2026.21. Do not mix executables and libraries from different versions.

## Original Project and Licensing

**Slang is an independent, open-source project.** Lumen RT is not the author of the Slang compiler and does not claim ownership of it.

- [Upstream source](https://github.com/shader-slang/slang)
- [Upstream v2026.21 release and full distributions](https://github.com/shader-slang/slang/releases/tag/v2026.21)
- License: **Apache License 2.0 with LLVM Exception** (`Apache-2.0 WITH LLVM-exception`)
- [Upstream v2026.21 license notice](https://github.com/shader-slang/slang/blob/v2026.21/LICENSE)
- [License notice in this repository](LICENSE)

The `LICENSE` file reproduces the matching upstream Slang license notice. **It does not establish the license for Lumen RT itself.** Full license texts and third-party notices from the matching official archives are included under [licenses](licenses) and in Lumen RT's bundled compiler resources.
