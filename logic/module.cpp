#include "logic/drone.hpp"
#include "logic/position.hpp"

#include <pybind11/pybind11.h>

PYBIND11_MODULE(logic, m) {
  m.doc() = "Drone logic written in C++";
  py_init_drone(m);
  py_position_init(m);
}
