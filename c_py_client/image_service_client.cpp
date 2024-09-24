#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <Python.h>

#include <grpcpp/grpcpp.h>
#include "image_service.grpc.pb.h"


using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using image_service::ImageService;
using image_service::ListImagesRequest;
using image_service::ListImagesResponse;

class ImageServiceClient {
 public:
  ImageServiceClient(std::shared_ptr<Channel> channel)
      : stub_(ImageService::NewStub(channel)) {}

  // Assembles the client's payload, sends it, and presents the response back
  // from the server.
  std::vector<std::string> ListImages() {
    ListImagesRequest request;
    ListImagesResponse reply;
    ClientContext context;

    Status status = stub_->ListImages(&context, request, &reply);

    // Act upon its status.
    if (status.ok()) {
      std::vector<std::string> image_names;
      for (const auto& image_name : reply.image_names()) {
        image_names.push_back(image_name);
      }
      return image_names;
    } else {
      std::cout << status.error_code() << ": " << status.error_message() << std::endl;
      return {};
    }
  }

 private:
  std::unique_ptr<ImageService::Stub> stub_;
};

struct ImageServiceClientCapsule {
  PyObject_HEAD;
  ImageServiceClient* client;
};

static PyObject* ImageServiceClient_new(PyTypeObject* type, PyObject* args,
                                        PyObject* kwds) {
  ImageServiceClientCapsule* self;
  self = (ImageServiceClientCapsule*)type->tp_alloc(type, 0);
  if (self == NULL) {
    return PyErr_NoMemory();
  }
  self->client = NULL;
  return (PyObject*)self;
}

static void createImageServiceClient(PyObject* self) {
  ImageServiceClientCapsule* capsule = (ImageServiceClientCapsule*)self;
  capsule->client = new ImageServiceClient(grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials()));
}

static void destroyImageServiceClient(PyObject* self) {
  ImageServiceClientCapsule* capsule = (ImageServiceClientCapsule*)self;
  delete capsule->client;
  capsule->client = NULL;
}

static void ImageServiceClient_dealloc(PyObject* self) {
  destroyImageServiceClient(self);
  Py_TYPE(self)->tp_free(self);
}

static PyObject* ImageServiceClient_ListImages(PyObject* self) {
  ImageServiceClientCapsule* capsule = (ImageServiceClientCapsule*)self;
  const auto image_names = capsule->client->ListImages();
  PyObject* list = PyList_New(image_names.size());
  for (size_t i = 0; i < image_names.size(); i++) {
    PyList_SetItem(list, i, PyUnicode_FromString(image_names[i].c_str()));
  }
  return list;
}

static PyMethodDef ImageServiceClient_methods[] = {
    {"__aenter__", (PyCFunction)createImageServiceClient, METH_NOARGS, ""},
    {"__aexit__", (PyCFunction)destroyImageServiceClient, METH_NOARGS, ""},
    {"list_images", (PyCFunction)ImageServiceClient_ListImages, METH_NOARGS, ""},
    {NULL, NULL, 0, NULL}};

static PyTypeObject ImageServiceClientType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "ImageServiceClient", /* tp_name */
    sizeof(ImageServiceClientCapsule), /* tp_basicsize */
    0,                                  /* tp_itemsize */
    (destructor)ImageServiceClient_dealloc, /* tp_dealloc */
    0,                                  /* tp_print */
    0,                                  /* tp_getattr */
    0,                                  /* tp_setattr */
    0,                                  /* tp_reserved */
    0,                                  /* tp_repr */
    0,                                  /* tp_as_number */
    0,                                  /* tp_as_sequence */
    0,                                  /* tp_as_mapping */
    0,                                  /* tp_hash  */
    0,                                  /* tp_call */
    0,                                  /* tp_str */
    0,                                  /* tp_getattro */
    0,                                  /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                 /* tp_flags */
    "ImageServiceClient",               /* tp_doc */
    0,                                  /* tp_traverse */
    0,                                 /* tp_clear */
    0,                                       /* tp_richcompare */
    0,                                       /* tp_weaklistoffset */
    0,                                       /* tp_iter */
    0,                                       /* tp_iternext */
    ImageServiceClient_methods,              /* tp_methods */
    0,                                       /* tp_members */
    0,                                       /* tp_getset */
    0,                                       /* tp_base */
    0,                                       /* tp_dict */
    0,                                       /* tp_descr_get */
    0,                                       /* tp_descr_set */
    0,                                       /* tp_dictoffset */
    0,                                       /* tp_init */
    PyType_GenericAlloc,                     /* tp_alloc */
    ImageServiceClient_new,                  /* tp_new */
    PyObject_GC_Del,                         /* tp_free */
};

static PyModuleDef ClientModuleDef = {PyModuleDef_HEAD_INIT,
                                     "image_service_client",
                                     NULL,
                                     -1,
                                     NULL,
                                     NULL,
                                     NULL,
                                     NULL,
                                     NULL};

PyMODINIT_FUNC PyInit_image_service_client(void) {
  PyObject* m;
  if (PyType_Ready(&ImageServiceClientType) < 0) {
    return NULL;
  }

  m = PyModule_Create(&ClientModuleDef);
  if (m == NULL) {
    return NULL;
  }

  Py_INCREF(&ImageServiceClientType);
  PyModule_AddObject(m, "ImageServiceClient", (PyObject*)&ImageServiceClientType);
  return m;
}

