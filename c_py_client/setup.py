from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class BuildExt(build_ext):
    def build_extensions(self):
        for ext in self.extensions:
            ext.extra_compile_args = ['-std=c++17']
            ext.extra_link_args = ["-lgrpc++", "-lgrpc", "-lgpr", "-lprotobuf"]
        build_ext.build_extensions(self)

setup(
    name='image_service_client',
    version='1.0',
    ext_modules=[
        Extension(
            'image_service_client',
            sources=[
                'image_service_client.cpp',
                'image_service.grpc.pb.cc',
                'image_service.pb.cc',
            ],
            libraries=['protobuf', 'grpc++', 'grpc'],
            library_dirs=['/usr/local/lib'],
            include_dirs=['.', '/usr/local/include'],
        )
    ],
    cmdclass={'build_ext': BuildExt},
)