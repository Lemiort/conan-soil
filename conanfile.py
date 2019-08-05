from conans import ConanFile, CMake, tools


class SoilConan(ConanFile):
    name = "soil"
    version = "1.1.1"
    license = "Public Domain"
    author = "Lemiort lemiort@gmail.com"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "Conan package for Simple Opengl Image Library"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = ["FindSOIL.cmake"]
    build_requires = "glew/2.1.0@bincrafters/stable"

    def source(self):
        self.run("git clone https://github.com/Lemiort/soil.git")
        self.run("cd soil && git checkout develop")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("soil/CMakeLists.txt", "include(build/conanbuildinfo.cmake)",
                              '''include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="soil")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/soil %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*SOIL.h", dst="include/SOIL", src="soil", keep_path=False)
        self.copy("*SOIL.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("FindSOIL.cmake", ".", ".")

    def package_info(self):
        self.cpp_info.libs = ["SOIL"]
