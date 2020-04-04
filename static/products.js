function Product(data) {
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
    this.timestamp = ko.observable(data.timestamp);
    this.price = ko.observable(data.price);
    this.image = ko.observable(data.image);
    this.category = ko.observable(data.category);
    this.description = ko.observable(data.description);
}

function ProductListViewModel() {
    var self = this;
    self.product_list = ko.observableArray([]);
    self.name= ko.observable();
    self.timestamp = ko.observable();
    self.price = ko.observable();
    self.image = ko.observable();
    self.category = ko.observable();
    self.description = ko.observable();


    self.addProduct = function() {
	self.save();
	self.name("");
	self.price("");
	self.image("");
	self.category("");
	self.description("");
    };

    $.getJSON('/api/v2/products', function(productModels) {
	var t = $.map(productModels.product_list, function(item) {
	    return new Product(item);
	});
	self.product_list(t);
    });

    self.save = function() {
	return $.ajax({
	    url: '/api/v2/products',
	    contentType: 'application/json',
	    type: 'POST',
	    data: JSON.stringify({
		'name': self.name(),
    'price': self.price(),
    'image': self.image(),
    'category': self.category(),
    'description': self.description(),
	    }),
	    success: function(data) {
          alert("success")
		      console.log("Pushing to array");
		      self.push(new Product({ name: data.name, price: data.price, image: data.image, category: data.category, description: data.description}));
		      return;
	    },
	    error: function() {
		return console.log("Failed");
	    }
	});
    };
}

ko.applyBindings(new ProductListViewModel());
