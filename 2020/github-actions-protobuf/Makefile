all:
	protoc --proto_path=. --cpp_out . person.proto
	g++ -std=c++17 person.pb.cc -c -o person.o
	g++ -std=c++17 main.cpp -c -o main.o
	g++ person.o main.o -o main -lprotobuf
