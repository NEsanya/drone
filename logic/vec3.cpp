#include "logic/vec3.hpp"

#include <sstream>

std::string Vec3::format() const {
  std::stringstream stream;
  stream << '(' << pos_.x << ", " << pos_.y << ", " << pos_.z << ')';
  return stream.str();
}

const float Vec3::distance_to(const Vec3 &to) const {
  return glm::distance(pos_, to.pos_);
}
const float Vec3::length() const { return glm::length(pos_); }

namespace py = pybind11;
void py_vec3_init(py::module_ &m) {
  py::class_<Vec3>(m, "Vec3", "Vec3 wrapper")
      .def(py::init<float, float, float>())
      .def(py::init<Vec3>())
      .def(py::init([](py::tuple t) {
             if (py::len(t) != 3)
               throw std::invalid_argument(
                   "Tuple size to cast to Vec3 must be 3");
             return std::make_unique<Vec3>(
                 t[0].cast<float>(), t[1].cast<float>(), t[2].cast<float>());
           }),
           "Tuple cast to Vec3")
      .def_property(
          "x", [](const Vec3 &pos) { return pos.x(); },
          [](Vec3 &pos, float value) { pos.x() = value; }, "X coordinate")
      .def_property(
          "y", [](const Vec3 &pos) { return pos.y(); },
          [](Vec3 &pos, float value) { pos.y() = value; }, "Y coordinate")
      .def_property(
          "z", [](const Vec3 &pos) { return pos.z(); },
          [](Vec3 &pos, float value) { pos.z() = value; }, "Z coordinate")
      .def("__repr__", &Vec3::format)
      .def("distance_to", &Vec3::distance_to,
           "Calculate distance from one vector to another")
      .def("length", &Vec3::length, "Vector length");
}
