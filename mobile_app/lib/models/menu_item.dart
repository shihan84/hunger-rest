class MenuItem {
  final int id;
  final String name;
  final double price;
  final String category;
  final double gstSlab;
  final String hsnCode;
  final String foodType;

  MenuItem({
    required this.id,
    required this.name,
    required this.price,
    required this.category,
    required this.gstSlab,
    required this.hsnCode,
    required this.foodType,
  });

  factory MenuItem.fromJson(Map<String, dynamic> json) {
    return MenuItem(
      id: json['id'],
      name: json['name'],
      price: json['price'].toDouble(),
      category: json['category'],
      gstSlab: json['gst_slab'].toDouble(),
      hsnCode: json['hsn_code'],
      foodType: json['food_type'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'price': price,
      'category': category,
      'gst_slab': gstSlab,
      'hsn_code': hsnCode,
      'food_type': foodType,
    };
  }
}
