import 'package:flutter/material.dart';
import 'create_order_screen.dart';

class TablesScreen extends StatefulWidget {
  @override
  _TablesScreenState createState() => _TablesScreenState();
}

class _TablesScreenState extends State<TablesScreen> {
  // Mock table data - would come from API
  final List<Map<String, dynamic>> tables = [
    {'number': 1, 'status': 'available', 'order_count': 0},
    {'number': 2, 'status': 'occupied', 'order_count': 1},
    {'number': 3, 'status': 'available', 'order_count': 0},
    {'number': 4, 'status': 'occupied', 'order_count': 2},
    {'number': 5, 'status': 'available', 'order_count': 0},
    {'number': 6, 'status': 'occupied', 'order_count': 1},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Tables',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 16),
            Expanded(
              child: GridView.builder(
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  childAspectRatio: 1.2,
                  crossAxisSpacing: 16,
                  mainAxisSpacing: 16,
                ),
                itemCount: tables.length,
                itemBuilder: (context, index) {
                  final table = tables[index];
                  return _buildTableCard(table);
                },
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Show table selection dialog
          _showTableSelectionDialog();
        },
        child: Icon(Icons.add),
        backgroundColor: Colors.orange.shade600,
      ),
    );
  }

  Widget _buildTableCard(Map<String, dynamic> table) {
    Color statusColor;
    IconData statusIcon;
    
    switch (table['status']) {
      case 'available':
        statusColor = Colors.green;
        statusIcon = Icons.check_circle;
        break;
      case 'occupied':
        statusColor = Colors.red;
        statusIcon = Icons.person;
        break;
      default:
        statusColor = Colors.grey;
        statusIcon = Icons.help;
    }

    return Card(
      elevation: 4,
      child: InkWell(
        onTap: () {
          _showTableDetails(table);
        },
        child: Padding(
          padding: EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.table_restaurant,
                size: 40,
                color: statusColor,
              ),
              SizedBox(height: 8),
              Text(
                'Table ${table['number']}',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(height: 4),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(statusIcon, size: 16, color: statusColor),
                  SizedBox(width: 4),
                  Text(
                    table['status'].toUpperCase(),
                    style: TextStyle(
                      color: statusColor,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
              if (table['order_count'] > 0) ...[
                SizedBox(height: 4),
                Text(
                  '${table['order_count']} order(s)',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  void _showTableDetails(Map<String, dynamic> table) {
    showModalBottomSheet(
      context: context,
      builder: (context) => Container(
        padding: EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'Table ${table['number']}',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 16),
            ListTile(
              leading: Icon(Icons.receipt_long),
              title: Text('View Orders'),
              onTap: () {
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('View Orders - Coming Soon')),
                );
              },
            ),
            ListTile(
              leading: Icon(Icons.add),
              title: Text('Create Order'),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => CreateOrderScreen(tableNumber: table['number']),
                  ),
                ).then((success) {
                  if (success == true) {
                    // Refresh table status or show success message
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text('Order created successfully!'),
                        backgroundColor: Colors.green,
                      ),
                    );
                  }
                });
              },
            ),
            if (table['status'] == 'occupied')
              ListTile(
                leading: Icon(Icons.payment),
                title: Text('Generate Bill'),
                onTap: () {
                  Navigator.pop(context);
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Generate Bill - Coming Soon')),
                  );
                },
              ),
          ],
        ),
      ),
    );
  }

  void _showTableSelectionDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Select Table'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: List.generate(10, (index) {
            final tableNumber = index + 1;
            return ListTile(
              title: Text('Table $tableNumber'),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => CreateOrderScreen(tableNumber: tableNumber),
                  ),
                ).then((success) {
                  if (success == true) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text('Order created successfully!'),
                        backgroundColor: Colors.green,
                      ),
                    );
                  }
                });
              },
            );
          }),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cancel'),
          ),
        ],
      ),
    );
  }
}
