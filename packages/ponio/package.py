from spack.package import *
import os


class Ponio(CMakePackage):
    """PONIO provides Runge–Kutta solvers and demos, including
    optional Samurai-based examples."""

    homepage = "https://github.com/hpc-maths/ponio"
    git = "https://github.com/hpc-maths/ponio.git"

    maintainers("sbstndbs")

    license("BSD-3-Clause")

    version("main", branch="main", preferred=True)
    version("0.2.0", tag="v0.2.0")

    variant("demos", default=True, description="Build C++ demos")
    variant(
        "samurai",
        default=True,
        description="Enable demos that depend on Samurai/PETSc",
    )

    depends_on("cmake@3.16:", type="build")
    depends_on("python@3.8:", type="build")
    depends_on("py-sympy", type="build")
    depends_on("py-numpy", type="build")
    depends_on("py-jinja2", type="build")
    depends_on("xtl@0.7.4")
    depends_on("xtensor@0.24.1")

    depends_on("samurai@0.26.1+mpi", when="+samurai")
    depends_on("petsc+mpi", when="+samurai")
    depends_on("boost+serialization+mpi", when="+samurai")
    depends_on("cli11", when="+samurai")
    depends_on("fmt", when="+samurai")
    depends_on("highfive+mpi", when="+samurai")
    depends_on("pugixml", when="+samurai")

    patch("fix-demos-samurai.patch", when="@0.2.0 +samurai")
    patch("fix-examples-samurai-main.patch", when="@main +samurai")

    @property
    def build_targets(self):
        if self.spec.satisfies("+samurai"):
            return ["bz_2d_pirock"]
        return []

    def install(self, spec, prefix):
        super().install(spec, prefix)
        if spec.satisfies('+samurai'):
            with working_dir(self.build_directory):
                bz_exec = join_path('ponio', 'examples', 'bz_2d_pirock')
                if os.path.isfile(bz_exec):
                    mkdirp(prefix.bin)
                    install(bz_exec, prefix.bin)

    def setup_build_environment(self, env):
        env.prepend_path('PYTHONPATH', join_path(self.stage.source_path, 'analysis'))

    @run_before("cmake")
    def patch_samurai_headers(self):
        if "+samurai" not in self.spec:
            return

        header = join_path(
            self.spec["samurai"].prefix.include, "samurai", "petsc", "utils.hpp"
        )
        if not os.path.exists(header):
            raise InstallError(
                "samurai header 'petsc/utils.hpp' not found; required for xtensor compatibility"
            )

        filter_file(
            r"#include <xtensor/xfixed.hpp>",
            "#include <xtensor/xfixed.hpp>\n#include <xtensor/xiterator.hpp>",
            header,
        )
        filter_file(
            r"container\.linear_begin\(\)",
            "xt::linear_begin(container)",
            header,
        )
        filter_file(
            r"container\.linear_end\(\)",
            "xt::linear_end(container)",
            header,
        )

    def cmake_args(self):
        spec = self.spec
        args = []

        args.append(self.define_from_variant("BUILD_DEMOS", "demos"))
        args.append(self.define_from_variant("BUILD_SAMURAI_DEMOS", "samurai"))
        args.append(self.define("ENABLE_VCPKG", False))
        args.append(self.define("ENABLE_CONAN_OPTION", False))
        args.append(self.define("BUILD_TESTS", False))
        args.append(self.define("BUILD_DOC", False))
        args.append(self.define("BUILD_OFFLINE", True))

        if spec.satisfies("+samurai"):
            args.append(self.define("SAMURAI_WITH_MPI", True))
            args.append(self.define("SAMURAI_FLUX_CONTAINER", "xtensor"))

        return args
