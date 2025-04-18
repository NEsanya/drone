#ifndef LOGIC_SRC_VEC3_HPP
#define LOGIC_SRC_VEC3_HPP

#include <glm/glm.hpp>
#include <pybind11/pybind11.h>

#include <string>

class Vec3 {
public:
  Vec3(float x, float y, float z) : pos_(x, y, z) {}
  Vec3(const Vec3 &pos) : pos_(pos.pos_) {}

  float &x() { return pos_.x; }
  const float x() const { return pos_.x; }
  float &y() { return pos_.y; }
  const float y() const { return pos_.y; }
  float &z() { return pos_.z; }
  const float z() const { return pos_.z; }

  std::string format() const;

  const float distance_to(const Vec3 &to) const;
  const float length() const;

private:
  glm::vec3 pos_;
};

void py_vec3_init(pybind11::module_ &m);

#endif // LOGIC_SRC_VEC3_HPP
