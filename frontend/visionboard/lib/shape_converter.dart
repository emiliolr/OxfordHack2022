import 'dart:math';

import 'package:visionboard/shape.dart';

class ShapeConverter {
  late Map<String, dynamic> _inputText;
  Random random = new Random(); // TODO: Remove the randomness

  ShapeConverter(Map<String, dynamic> inputText) {
    _inputText = inputText;
    print('Result of post request: '+inputText.toString());
  }

  List<MyShape> getListOfShapes() {
    List<MyShape> shapes = [];

    print(_inputText);

    _inputText.forEach((key, value) {
      if (key == 'circle') {
        shapes.add(Circle(
            shapeName: key,
            color: value['color'],
            radius: value['radius'] * 1.0,
            x_center: value['center'][0] * 1.0,
            y_center: value['center'][1] * 1.0,
            fill: true));
      } else if (key == 'square') {
        shapes.add(Rectangle(
            shapeName: 'rectangle',
            color: value['color'],
            x_start: value['top_left'][0] * 1.0,
            y_start: value['top_left'][1] * 1.0,
            width: value['side_length'] * 1.0,
            height: value['side_length'] * 1.0,
            fill: false));
      }
    });

    return shapes;
  }
}
