# spack_ponio

Custom Spack repository that provides a `ponio` package able to build the Belousov–Zhabotinsky 2D example with Samurai support.

## Layout

- `repo.yaml`: declares the `spack_ponio` namespace so Spack can register the repo.
- `packages/ponio/`: contains the package recipe and Samurai compatibility patches.

## Usage

```bash
spack repo add /path/to/spack_ponio/repo
spack install ponio@main
spack load ponio
bz_2d_pirock  # written by the install() helper into $SPACK_PREFIX/bin
```

Variants are enabled by default to build the C++ demos and the Samurai-based examples.  Building without Samurai is still possible with `~samurai`.

## What Works

- `ponio@main +samurai`: successfully builds with Samurai 0.26.1, PETSc and MPI, and installs the `bz_2d_pirock` executable under `prefix/bin`.
- `ponio@0.2.0 ~samurai`: builds as a pure library (the patch `fix-demos-samurai.patch` is only applied when Samurai demos are requested).

## Outstanding Issues & Notes

- Ponio’s upstream CMakeLists do not set `SAMURAI_FLUX_CONTAINER`; Samurai ≥0.26 errors out unless the package forces the value to `xtensor`. The Spack recipe injects this flag and applies a patch ensuring the demos request the necessary dependencies (CLI11, PETSc includes/flags, etc.).
- Samurai’s PETSc headers currently miss the `xtensor` iterator include and still call `container.linear_begin/end()`. The package’s `patch_samurai_headers()` hook rewrites `samurai/petsc/utils.hpp` inside the activated Samurai installation to restore the behaviour required by Ponio.
- Updating Samurai to a newer commit may eliminate the need for these workarounds; when that happens the patches/install hook should be revisited.
- The repository does not yet package the Python scripts or the optional visualisation helpers that live alongside the demos.

## Next steps (optional)

1. Submit the CMake fixes upstream (Ponio/Samurai) so the Spack recipe can drop the patch stack.
2. Add smoke tests that exercise `bz_2d_pirock` or other demos after installation.
3. Extend the package to expose Ponio’s Python tooling and datasets if needed.
