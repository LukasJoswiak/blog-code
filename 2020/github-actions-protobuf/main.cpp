#include <iostream>

#include "person.pb.h"

int main() {
  Person p;
  p.set_name("Person");
  p.set_id(1);
  std::cout << "Hello, " << p.DebugString() << std::endl;
}
