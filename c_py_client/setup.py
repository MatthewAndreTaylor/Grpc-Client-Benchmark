from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class BuildExt(build_ext):
    def build_extensions(self):
        for ext in self.extensions:
            ext.extra_compile_args = ['-std=c++17', '-pthread', '-I/usr/local/include']
            ext.extra_link_args = ['-L/usr/local/lib', '-lgrpc++', '-lgrpc', '-lprotobuf', '-lpthread', '-ldl']
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
            language='c++',
        )
    ],
    cmdclass={'build_ext': BuildExt},
)