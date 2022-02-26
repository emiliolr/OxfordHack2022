// Extend this class to specific shape implementations so that we can create a
// list of different shapes
class MyShape {
  String shapeName = '';
  String color = '';

  MyShape({required this.shapeName, required this.color});
}

// Circle constructor has information about radius, x center, y center,
// and whether or not to fill the shape
class Circle extends MyShape {
  double radius;
  double x_center;
  double y_center;
  bool fill;

  Circle(
      {required String shapeName,
      required String color,
      required double this.radius,
      required double this.x_center,
      required double this.y_center,
      required bool this.fill})
      : super(shapeName: shapeName, color: color);
}

// Rectangle constructor has information about x start, y start, width, height,
// and whether or not to fill the shape
class Rectangle extends MyShape {
  double x_start;
  double y_start;
  double width;
  double height;
  bool fill;

  Rectangle(
      {required String shapeName,
      required String color,
      required double this.x_start,
      required double this.y_start,
      required double this.width,
      required double this.height,
      required bool this.fill})
      : super(shapeName: shapeName, color: color);
}
