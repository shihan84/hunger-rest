class OrderItem {
  final int id;
  final String name;
  final double rate;
  final double gstSlab;
  final String hsnCode;
  int quantity;

  OrderItem({
    required this.id,
    required this.name,
    required this.rate,
    required this.gstSlab,
    required this.hsnCode,
    this.quantity = 1,
  });

  factory OrderItem.fromMenuItem(MenuItem menuItem, {int quantity = 1}) {
    return OrderItem(
      id: menuItem.id,
      name: menuItem.name,
      rate: menuItem.price,
      gstSlab: menuItem.gstSlab,
      hsnCode: menuItem.hsnCode,
      quantity: quantity,
    );
  }

  double get total => rate * quantity;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'rate': rate,
      'gst_slab': gstSlab,
      'hsn_code': hsnCode,
      'quantity': quantity,
    };
  }
}
