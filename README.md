# Lumen RT — Runtime Dependencies

This repository hosts third-party runtime components used by **Lumen RT**, a Minecraft Java Edition Vulkan-based ray tracing mod.

## Slang Compiler (Windows x64)

The release contains **`slangc.exe` v2026.8**, the unmodified Slang shader compiler from the official [Slang project](https://github.com/shader-slang/slang).

Lumen RT uses it to compile certain shaders at runtime, including shaders needed to support custom rendering effects from other mods. The executable is distributed separately because CurseForge does not allow `.exe` files inside mod JARs.

Lumen RT is being updated to download this executable automatically when Minecraft starts. **Manual installation is not intended to be required.**

### Download

- [Download `slangc.exe` v2026.8 (Windows x64)](https://github.com/rmiss1/lumenrt-dependencies/releases/download/slangc-windows-x64-v2026.8/slangc.exe)
- [Release details](https://github.com/rmiss1/lumenrt-dependencies/releases/tag/slangc-windows-x64-v2026.8)
- **SHA-256:** `a3bfe7b61fe2bd67cc7408f81fd7663cfca55e369591f55b0d2327c5c8c5f015`

The SHA-256 value above identifies the specific file published in this release. It is intended for integrity verification before execution.

## Original Project and Licensing

**Slang is an independent, open-source project.** Lumen RT is not the author of the Slang compiler and does not claim ownership of it.

- Upstream source: https://github.com/shader-slang/slang
- Upstream version: https://github.com/shader-slang/slang/releases/tag/v2026.8
- Slang's license: **Apache License 2.0 with LLVM Exception** (`Apache-2.0 WITH LLVM-exception`)
- [Upstream license text for v2026.8](https://github.com/shader-slang/slang/blob/v2026.8/LICENSE)
- [License text in this repository](LICENSE)

The `LICENSE` file reproduces the upstream Slang license notice for the redistributed compiler. **It does not establish the license for Lumen RT itself.** The compiler may incorporate third-party components subject to their own notices and licenses; these should be preserved from the matching official Slang distribution.

## Platform Compatibility

This release asset targets **Windows x64**. The Slang compiler also depends on compatible runtime DLLs; the executable is not a standalone replacement for its matching libraries.
