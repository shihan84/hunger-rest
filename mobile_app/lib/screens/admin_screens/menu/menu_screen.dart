import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../services/api_service.dart';
import '../../../models/menu_item.dart';

class MenuScreen extends StatefulWidget {
	@override
	_MenuScreenState createState() => _MenuScreenState();
}

class _MenuScreenState extends State<MenuScreen> {
	List<MenuItem> _items = [];
	bool _loading = true;
	String? _error;

	@override
	void initState() {
		super.initState();
		_refresh();
	}

	Future<void> _refresh() async {
		setState(() { _loading = true; _error = null; });
		try {
			final api = Provider.of<ApiService>(context, listen: false);
			final items = await api.getMenuItems();
			setState(() { _items = items; _loading = false; });
		} catch (e) {
			setState(() { _error = e.toString(); _loading = false; });
		}
	}

	void _openAddDialog() async {
		final result = await showDialog<MenuItem>(
			context: context,
			builder: (context) => _MenuItemDialog(),
		);
		if (result != null) {
			await _createItem(result);
		}
	}

	Future<void> _createItem(MenuItem item) async {
		try {
			final api = Provider.of<ApiService>(context, listen: false);
			// POST /api/menu
			final resp = await api.createMenuItem(item);
			if (mounted) {
				ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Item created')));
				_refresh();
			}
		} catch (e) {
			if (mounted) {
				ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed: $e')));
			}
		}
	}

	void _openEditDialog(MenuItem existing) async {
		final result = await showDialog<MenuItem>(
			context: context,
			builder: (context) => _MenuItemDialog(existing: existing),
		);
		if (result != null) {
			await _updateItem(existing.id, result);
		}
	}

	Future<void> _updateItem(int id, MenuItem item) async {
		try {
			final api = Provider.of<ApiService>(context, listen: false);
			await api.updateMenuItem(id, item);
			if (mounted) {
				ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Item updated')));
				_refresh();
			}
		} catch (e) {
			if (mounted) {
				ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed: $e')));
			}
		}
	}

	Future<void> _deleteItem(int id) async {
		try {
			final api = Provider.of<ApiService>(context, listen: false);
			await api.deleteMenuItem(id);
			if (mounted) {
				ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Item deleted')));
				_refresh();
			}
		} catch (e) {
			if (mounted) {
				ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed: $e')));
			}
		}
	}

	@override
	Widget build(BuildContext context) {
		return Scaffold(
			appBar: AppBar(
				title: Text('Menu Management'),
				backgroundColor: Colors.orange.shade600,
				actions: [
					IconButton(onPressed: _refresh, icon: Icon(Icons.refresh)),
				],
			),
			floatingActionButton: FloatingActionButton(
				onPressed: _openAddDialog,
				child: Icon(Icons.add),
				backgroundColor: Colors.orange.shade600,
			),
			body: _loading
				? Center(child: CircularProgressIndicator())
				: _error != null
					? Center(child: Text('Error: $_error'))
					: ListView.separated(
						itemCount: _items.length,
						separatorBuilder: (_, __) => Divider(height: 1),
						itemBuilder: (context, index) {
							final item = _items[index];
							return ListTile(
								title: Text(item.name),
								subtitle: Text('₹${item.price.toStringAsFixed(2)} • ${item.category} • ${item.foodType}'),
								trailing: Row(
									mainAxisSize: MainAxisSize.min,
									children: [
										IconButton(icon: Icon(Icons.edit), onPressed: () => _openEditDialog(item)),
										IconButton(icon: Icon(Icons.delete, color: Colors.red), onPressed: () => _deleteItem(item.id)),
									],
								),
							);
						},
					),
		);
	}
}

class _MenuItemDialog extends StatefulWidget {
	final MenuItem? existing;
	_MenuItemDialog({this.existing});
	@override
	State<_MenuItemDialog> createState() => _MenuItemDialogState();
}

class _MenuItemDialogState extends State<_MenuItemDialog> {
	final _formKey = GlobalKey<FormState>();
	final _nameCtrl = TextEditingController();
	final _priceCtrl = TextEditingController();
	final _categoryCtrl = TextEditingController();
	final _gstCtrl = TextEditingController(text: '5');
	final _hsnCtrl = TextEditingController(text: '996331');
	String _foodType = 'veg';

	@override
	void initState() {
		super.initState();
		if (widget.existing != null) {
			_nameCtrl.text = widget.existing!.name;
			_priceCtrl.text = widget.existing!.price.toStringAsFixed(2);
			_categoryCtrl.text = widget.existing!.category;
			_gstCtrl.text = widget.existing!.gstSlab.toString();
			_hsnCtrl.text = widget.existing!.hsnCode;
			_foodType = widget.existing!.foodType;
		}
	}

	@override
	Widget build(BuildContext context) {
		return AlertDialog(
			title: Text(widget.existing == null ? 'Add Menu Item' : 'Edit Menu Item'),
			content: SingleChildScrollView(
				child: Form(
					key: _formKey,
					child: Column(
						mainAxisSize: MainAxisSize.min,
						children: [
							TextFormField(
								controller: _nameCtrl,
								decoration: InputDecoration(labelText: 'Name'),
								validator: (v) => v == null || v.isEmpty ? 'Required' : null,
							),
							TextFormField(
								controller: _priceCtrl,
								keyboardType: TextInputType.number,
								decoration: InputDecoration(labelText: 'Price'),
								validator: (v) => v == null || v.isEmpty ? 'Required' : null,
							),
							TextFormField(
								controller: _categoryCtrl,
								decoration: InputDecoration(labelText: 'Category'),
								validator: (v) => v == null || v.isEmpty ? 'Required' : null,
							),
							Row(
								children: [
									Expanded(
										child: TextFormField(
											controller: _gstCtrl,
											keyboardType: TextInputType.number,
											decoration: InputDecoration(labelText: 'GST %'),
											validator: (v) => v == null || v.isEmpty ? 'Required' : null,
										),
									),
									SizedBox(width: 8),
									Expanded(
										child: TextFormField(
											controller: _hsnCtrl,
											decoration: InputDecoration(labelText: 'HSN Code'),
											validator: (v) => v == null || v.isEmpty ? 'Required' : null,
										),
									),
								],
							),
							DropdownButtonFormField<String>(
								value: _foodType,
								items: const [
									DropdownMenuItem(value: 'veg', child: Text('Veg')),
									DropdownMenuItem(value: 'non-veg', child: Text('Non-Veg')),
								],
								onChanged: (v) => setState(() => _foodType = v ?? 'veg'),
								decoration: InputDecoration(labelText: 'Type'),
							),
						],
					),
				),
			),
			actions: [
				TextButton(onPressed: () => Navigator.pop(context), child: Text('Cancel')),
				ElevatedButton(
					onPressed: () {
						if (_formKey.currentState!.validate()) {
							final price = double.tryParse(_priceCtrl.text.trim()) ?? 0.0;
							final gst = double.tryParse(_gstCtrl.text.trim()) ?? 0.0;
							final item = MenuItem(
								id: widget.existing?.id ?? 0,
								name: _nameCtrl.text.trim(),
								price: price,
								category: _categoryCtrl.text.trim(),
								gstSlab: gst,
								hsnCode: _hsnCtrl.text.trim(),
								foodType: _foodType,
							);
							Navigator.pop(context, item);
						}
					},
					child: Text(widget.existing == null ? 'Create' : 'Save'),
				),
			],
		);
	}
}
