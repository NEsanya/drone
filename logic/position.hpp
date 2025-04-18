#ifndef LOGIC_SRC_POSITION_HPP
#define LOGIC_SRC_POSITION_HPP

#include <glm/glm.hpp>
#include <pybind11/pybind11.h>

#include <string>

class Position {
public:
  Position(float x, float y, float z) : pos_(x, y, z) {}
  Position(const Position &pos) : pos_(pos.pos_) {}

  float &x() { return pos_.x; }
  const float x() const { return pos_.x; }
  float &y() { return pos_.y; }
  const float y() const { return pos_.y; }
  float &z() { return pos_.z; }
  const float z() const { return pos_.z; }

  std::string format() const;

private:
  glm::vec3 pos_;
};

void py_position_init(pybind11::module_ &m);

#endif // LOGIC_SRC_POSITION_HPP
