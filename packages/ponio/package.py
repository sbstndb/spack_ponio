from spack.package import *


class Ponio(CMakePackage):
    """PONIO provides Runge–Kutta solvers and demos."""

    homepage = "https://github.com/hpc-maths/ponio"
    git = "https://github.com/hpc-maths/ponio.git"

    maintainers("sbstndbs")

    license("BSD-3-Clause")

    version("main", branch="main", preferred=True)
    version("0.2.0", tag="v0.2.0")

    variant("demos", default=True, description="Build C++ demos")
    variant("tests", default=False, description="Build unit tests")

    depends_on("cmake@3.28.2:3.28", type="build")
    depends_on("python@3.8:", type="build")
    depends_on("py-sympy@1.12:1", type="build")
    depends_on("py-numpy@1.26.3:1.26", type="build")
    depends_on("py-jinja2@3.1.3:3.1", type="build")
    depends_on("pkgconf@0.29.2:", type="build")
    depends_on("eigen@3.4:3.4")
    depends_on("cli11@2.3.2:2.3", when="+demos")
    depends_on("doctest@2.4.11:2.4", when="+tests", type="build")

    def setup_build_environment(self, env):
        env.prepend_path('PYTHONPATH', join_path(self.stage.source_path, 'analysis'))

    def cmake_args(self):
        spec = self.spec
        args = []

        args.append(self.define_from_variant("BUILD_DEMOS", "demos"))
        args.append(self.define("BUILD_SAMURAI_DEMOS", False))
        args.append(self.define("ENABLE_VCPKG", False))
        args.append(self.define("ENABLE_CONAN_OPTION", False))
        args.append(self.define("BUILD_TESTS", spec.satisfies("+tests")))
        args.append(self.define("BUILD_DOC", False))
        args.append(self.define("BUILD_OFFLINE", True))

        return args
