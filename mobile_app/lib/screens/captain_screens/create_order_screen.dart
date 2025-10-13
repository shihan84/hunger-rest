import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../models/menu_item.dart';
import '../../models/order_item.dart';
import '../../services/api_service.dart';
import '../../services/auth_service.dart';

class CreateOrderScreen extends StatefulWidget {
  final int tableNumber;

  const CreateOrderScreen({Key? key, required this.tableNumber}) : super(key: key);

  @override
  _CreateOrderScreenState createState() => _CreateOrderScreenState();
}

class _CreateOrderScreenState extends State<CreateOrderScreen> {
  List<MenuItem> _menuItems = [];
  List<OrderItem> _cartItems = [];
  bool _isLoading = true;
  String? _error;
  ApiService? _apiService;

  @override
  void initState() {
    super.initState();
    _loadMenuItems();
  }

  Future<void> _loadMenuItems() async {
    try {
      final authService = Provider.of<AuthService>(context, listen: false);
      _apiService = ApiService(authService);
      final items = await _apiService!.getMenuItems();
      setState(() {
        _menuItems = items;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  void _addToCart(MenuItem item) {
    setState(() {
      final existingIndex = _cartItems.indexWhere((cartItem) => cartItem.id == item.id);
      if (existingIndex != -1) {
        _cartItems[existingIndex].quantity++;
      } else {
        _cartItems.add(OrderItem.fromMenuItem(item));
      }
    });
  }

  void _removeFromCart(OrderItem item) {
    setState(() {
      final index = _cartItems.indexWhere((cartItem) => cartItem.id == item.id);
      if (index != -1) {
        if (_cartItems[index].quantity > 1) {
          _cartItems[index].quantity--;
        } else {
          _cartItems.removeAt(index);
        }
      }
    });
  }

  double get _cartTotal {
    return _cartItems.fold(0.0, (sum, item) => sum + item.total);
  }

  Future<void> _submitOrder() async {
    if (_cartItems.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please add items to cart')),
      );
      return;
    }

    try {
      final invoiceNumber = await _apiService!.createOrder(
        tableNumber: widget.tableNumber,
        items: _cartItems,
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Order created successfully: $invoiceNumber'),
            backgroundColor: Colors.green,
          ),
        );
        Navigator.pop(context, true); // Return true to indicate success
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to create order: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Table ${widget.tableNumber} - Create Order'),
        backgroundColor: Colors.orange.shade600,
        actions: [
          if (_cartItems.isNotEmpty)
            Stack(
              children: [
                IconButton(
                  icon: Icon(Icons.shopping_cart),
                  onPressed: () => _showCartBottomSheet(),
                ),
                Positioned(
                  right: 8,
                  top: 8,
                  child: Container(
                    padding: EdgeInsets.all(2),
                    decoration: BoxDecoration(
                      color: Colors.red,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    constraints: BoxConstraints(
                      minWidth: 16,
                      minHeight: 16,
                    ),
                    child: Text(
                      '${_cartItems.length}',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 12,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ),
              ],
            ),
        ],
      ),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.error, size: 64, color: Colors.red),
                      SizedBox(height: 16),
                      Text('Error: $_error'),
                      SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: _loadMenuItems,
                        child: Text('Retry'),
                      ),
                    ],
                  ),
                )
              : _buildMenuGrid(),
      bottomNavigationBar: _cartItems.isNotEmpty
          ? Container(
              padding: EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                boxShadow: [
                  BoxShadow(
                    color: Colors.black26,
                    blurRadius: 10,
                    offset: Offset(0, -5),
                  ),
                ],
              ),
              child: Row(
                children: [
                  Expanded(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Total: ₹${_cartTotal.toStringAsFixed(2)}',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          '${_cartItems.length} item(s)',
                          style: TextStyle(
                            color: Colors.grey[600],
                          ),
                        ),
                      ],
                    ),
                  ),
                  ElevatedButton(
                    onPressed: _submitOrder,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.orange.shade600,
                      padding: EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                    ),
                    child: Text(
                      'Place Order',
                      style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
            )
          : null,
    );
  }

  Widget _buildMenuGrid() {
    // Group items by category
    final Map<String, List<MenuItem>> categorizedItems = {};
    for (final item in _menuItems) {
      if (!categorizedItems.containsKey(item.category)) {
        categorizedItems[item.category] = [];
      }
      categorizedItems[item.category]!.add(item);
    }

    return ListView.builder(
      itemCount: categorizedItems.length,
      itemBuilder: (context, categoryIndex) {
        final category = categorizedItems.keys.elementAt(categoryIndex);
        final items = categorizedItems[category]!;

        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: EdgeInsets.all(16),
              child: Text(
                category,
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            GridView.builder(
              shrinkWrap: true,
              physics: NeverScrollableScrollPhysics(),
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                childAspectRatio: 0.8,
                crossAxisSpacing: 8,
                mainAxisSpacing: 8,
              ),
              padding: EdgeInsets.symmetric(horizontal: 16),
              itemCount: items.length,
              itemBuilder: (context, index) {
                final item = items[index];
                return _buildMenuItemCard(item);
              },
            ),
            SizedBox(height: 16),
          ],
        );
      },
    );
  }

  Widget _buildMenuItemCard(MenuItem item) {
    final cartItem = _cartItems.firstWhere(
      (cartItem) => cartItem.id == item.id,
      orElse: () => OrderItem.fromMenuItem(item, quantity: 0),
    );

    return Card(
      elevation: 2,
      child: InkWell(
        onTap: () => _addToCart(item),
        child: Padding(
          padding: EdgeInsets.all(8),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Container(
                  width: double.infinity,
                  decoration: BoxDecoration(
                    color: Colors.grey[100],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    item.foodType == 'veg' ? Icons.eco : Icons.restaurant,
                    size: 32,
                    color: item.foodType == 'veg' ? Colors.green : Colors.red,
                  ),
                ),
              ),
              SizedBox(height: 8),
              Text(
                item.name,
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 14,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              SizedBox(height: 4),
              Text(
                '₹${item.price.toStringAsFixed(2)}',
                style: TextStyle(
                  color: Colors.orange.shade600,
                  fontWeight: FontWeight.bold,
                ),
              ),
              if (cartItem.quantity > 0) ...[
                SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    IconButton(
                      icon: Icon(Icons.remove_circle, color: Colors.red),
                      onPressed: () => _removeFromCart(cartItem),
                      padding: EdgeInsets.zero,
                      constraints: BoxConstraints(),
                    ),
                    Text(
                      '${cartItem.quantity}',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                      ),
                    ),
                    IconButton(
                      icon: Icon(Icons.add_circle, color: Colors.green),
                      onPressed: () => _addToCart(item),
                      padding: EdgeInsets.zero,
                      constraints: BoxConstraints(),
                    ),
                  ],
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  void _showCartBottomSheet() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (context) => Container(
        height: MediaQuery.of(context).size.height * 0.7,
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Cart Items',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 16),
            Expanded(
              child: ListView.builder(
                itemCount: _cartItems.length,
                itemBuilder: (context, index) {
                  final item = _cartItems[index];
                  return ListTile(
                    title: Text(item.name),
                    subtitle: Text('₹${item.rate.toStringAsFixed(2)} each'),
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        IconButton(
                          icon: Icon(Icons.remove_circle),
                          onPressed: () => _removeFromCart(item),
                        ),
                        Text(
                          '${item.quantity}',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        IconButton(
                          icon: Icon(Icons.add_circle),
                          onPressed: () => _addToCart(MenuItem(
                            id: item.id,
                            name: item.name,
                            price: item.rate,
                            category: '',
                            gstSlab: item.gstSlab,
                            hsnCode: item.hsnCode,
                            foodType: '',
                          )),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
            Divider(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Total: ₹${_cartTotal.toStringAsFixed(2)}',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                ElevatedButton(
                  onPressed: _submitOrder,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.orange.shade600,
                  ),
                  child: Text(
                    'Place Order',
                    style: TextStyle(color: Colors.white),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
