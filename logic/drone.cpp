#include "logic/drone.hpp"

#include "logic/vec3.hpp"

namespace py = pybind11;

class Drone {
public:
  Vec3 linear_speed, angle_speed, angle, pos;

  Drone(const py::kwargs &kwargs) noexcept
      : linear_speed(kwargs2vec(kwargs, "linear_speed")),
        angle_speed(kwargs2vec(kwargs, "angle_speed")),
        angle(kwargs2vec(kwargs, "angle")), pos(kwargs2vec(kwargs, "pos")) {}

  void update_data(Vec3 linear_speed, Vec3 angle_speed, Vec3 angle, Vec3 pos);

private:
  static Vec3 kwargs2vec(py::dict d, const char *name) {
    if (!d.contains(name))
      return Vec3(0, 0, 0);
    auto t = d[name].cast<py::tuple>();

    if (py::len(t) != 3)
      throw std::invalid_argument("Invalid tuple size for Vec3");
    return Vec3(t[0].cast<float>(), t[1].cast<float>(), t[2].cast<float>());
  }
};

void Drone::update_data(Vec3 linear_speed_, Vec3 angle_speed_, Vec3 angle_,
                        Vec3 pos_) {
  linear_speed = linear_speed_;
  angle_speed = angle_speed_;
  angle = angle_;
  pos = pos_;
}

void py_init_drone(py::module_ &m) {
  py::class_<Drone>(m, "Drone", "The main class for drone entity")
      .def(py::init<const py::kwargs &>())
      .def_readonly("linear_speed", &Drone::linear_speed,
                    "Linear speed of the drone")
      .def_readonly("angle_speed", &Drone::angle_speed,
                    "Angle speed of the drone")
      .def_readonly("angle", &Drone::angle, "Anglt of the drone")
      .def_readonly("pos", &Drone::pos, "Position of the drone")
      .def("__repr__",
           [](const Drone &drone) {
             return "<logic.Drone at " + drone.pos.format() + '>';
           })
      .def("update_data", &Drone::update_data, py::kw_only(),
           py::arg("linear_speed"), py::arg("angle_speed"), py::arg("angle"),
           py::arg("pos"), "Updating drone data");
}
