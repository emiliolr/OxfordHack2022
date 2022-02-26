import 'dart:math';

import 'package:visionboard/shape.dart';

class ShapeConverter {
  List<String> _inputText = [];
  Random random = new Random(); // TODO: Remove the randomness

  ShapeConverter(List<String> inputText) {
    _inputText = inputText;
  }

  List<MyShape> getListOfShapes() {
    List<MyShape> shapes = [];

    _inputText.forEach((String shape) {
      if (shape == 'circle') {
        shapes.add(Circle(
            shapeName: shape,
            color: '#ff0000',
            radius: 30.0,
            x_center: random.nextInt(100) * 1.0,
            y_center: random.nextInt(100) * 1.0,
            fill: true));
      } else if (shape == 'rectangle') {
        shapes.add(Rectangle(
            shapeName: shape,
            color: '#00ff00',
            x_start: random.nextInt(100) * 1.0,
            y_start: random.nextInt(100) * 1.0,
            width: 50.0,
            height: 50.0,
            fill: false));
      }
    });

    return shapes;
  }
}
