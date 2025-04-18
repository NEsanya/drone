#include "logic/drone.hpp"

#include "logic/position.hpp"

#include <string>

class Drone {
public:
  Position pos;
  Drone(const std::string &name) noexcept : pos(0, 0, 0), name_(name) {}

  void set_name(const std::string &name) { name_ = name; }
  const std::string &get_name() const { return name_; }
  void go(Position to) noexcept { pos = Position(to); }

private:
  std::string name_;
};

namespace py = pybind11;
void py_init_drone(py::module_ &m) {
  py::class_<Drone>(m, "Drone", "The main class for drone entity")
      .def(py::init<const std::string &>(), "Creates new drone entity")
      .def_property_readonly("name", &Drone::get_name, "Drone name")
      .def_readonly("pos", &Drone::pos, "Position of the drone")
      .def("go", &Drone::go, "Go to a position")
      .def("__repr__", [](const Drone &drone) {
        return "<logic.Drone named '" + drone.get_name() + "' at " +
               drone.pos.format() + '>';
      });
}
