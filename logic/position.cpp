#include "logic/position.hpp"

#include <sstream>

std::string Position::format() const {
  std::stringstream stream;
  stream << '(' << pos_.x << ", " << pos_.y << ", " << pos_.z << ')';
  return stream.str();
}

namespace py = pybind11;
void py_position_init(py::module_ &m) {
  py::class_<Position>(m, "Position", "An entity position (vec3 basically)")
      .def(py::init<float, float, float>())
      .def(py::init<Position>())
      .def_property(
          "x", [](const Position &pos) { return pos.x(); },
          [](Position &pos, float value) { pos.x() = value; }, "X coordinate")
      .def_property(
          "y", [](const Position &pos) { return pos.y(); },
          [](Position &pos, float value) { pos.y() = value; }, "Y coordinate")
      .def_property(
          "z", [](const Position &pos) { return pos.z(); },
          [](Position &pos, float value) { pos.z() = value; }, "Z coordinate")
      .def("__repr__", &Position::format);
}
