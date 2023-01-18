$(document).ready(function() {
	// jquery cho onTop
	$(document).scroll(function() {
		if ($(document).scrollTop() != 0) {
			$("#onTop").fadeIn();
		} else {
			$("#onTop").fadeOut();
		}
	});
	$("#onTop").click(function() {
		$("html, body").animate({ scrollTop: 0 }, 700);
	});

	$("#myInput").on("keyup", function() {
		var value = $(this).val().toLowerCase();
		$("#myTable tr").filter(function() {
			$(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
		});
	});

});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

var Shop = {
	addToCart: function(barCode) {
		var data = {};
		data["barCode"] = barCode;

		$.ajax({
			headers: {'X-CSRFToken': csrftoken},
			url: "/rest/api/cart/addToCart/",
			type: "post",
			contentType: "application/json",
			data: JSON.stringify(data),

			dataType: "json",
			success: function(jsonResult) {
				if (jsonResult.barCode == 'login') {
					location.href = "/login/";
				} else {
					alert("Bạn đã thêm hàng thành công");
					$("span.count-item").html(jsonResult.totalQuantity);
				}
			}
		});
	},

	addToCartNow: function(barCode) {
		var data = {};
		data["barCode"] = barCode;

		$.ajax({
			headers: {'X-CSRFToken': csrftoken},
			url: "/rest/api/cart/addToCart/",
			type: "post",
			contentType: "application/json",
			data: JSON.stringify(data),

			dataType: "json",
			success: function(jsonResult) {
				if (jsonResult.barCode == 'login') {
					location.href = "/login/";
				} else {
					location.href = "/cart/";
					$("span.count-item").html(jsonResult.totalQuantity);
				}
			}
		});
	},

	deleteCart: function(barCode) {
		var flag = confirm("Bạn có chắc chắn muốn xóa sản phẩm này khỏi giỏ hàng?");
		if (flag == true) {
			var data = {};
			data["barCode"] = barCode;

			$.ajax({
				headers: {'X-CSRFToken': csrftoken},
				url: "/rest/api/cart/deleteCart/",
				type: "post",
				contentType: "application/json",
				data: JSON.stringify(data),

				dataType: "json",
				success: function(jsonResult) {
					if (jsonResult.barCode == 'login') {
						location.href = "/login/";
					} else {
						location.href = "/cart/";
					}
				}
			});
		}
	},

	editCart: function(barCode) {
		var quantity = $("#quantity" + barCode).val();
		var data = {};
		data["quantity"] = quantity;
		data["barCode"] = barCode;

		$.ajax({
			headers: {'X-CSRFToken': csrftoken},
			url: "/rest/api/cart/editCart/",
			type: "post",
			contentType: "application/json",
			data: JSON.stringify(data),

			dataType: "json",
			success: function(jsonResult) {
				if (jsonResult.barCode == 'login') {
					location.href = "/login/";
				} else {
					$("span.count-item").html(jsonResult.totalQuantity);
					$("#price" + barCode).html(new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND'}).format(jsonResult.price));
					$("#total_value").html(new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND'}).format(jsonResult.totalAmount));
				}
			}
		});
	},

	goNext() {
		var tech = Shop.getUrlParameter('page') || 1;
		Shop.addUrlParameter('page', (parseInt(tech) + 1));
	},

	getUrlParameter: function(sParam) {
		var sPageURL = window.location.search.substring(1),
			sURLVariables = sPageURL.split('&'),
			sParameterName,
			i;

		for (i = 0; i < sURLVariables.length; i++) {
			sParameterName = sURLVariables[i].split('=');

			if (sParameterName[0] === sParam) {
				return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
			}
		}
	},

	goPrev() {
		var tech = Shop.getUrlParameter('page') || 1;
		if (parseInt(tech) > 1)
			Shop.addUrlParameter('page', (parseInt(tech) - 1));

	},

	addUrlParameter(name, value) {
		var searchParams = new URLSearchParams(window.location.search);
		searchParams.set(name, value);
		window.location.search = searchParams.toString();
	},

	deleteUrlParameter(name) {
		var searchParams = new URLSearchParams(window.location.search);
		searchParams.delete(name);
		window.location.search = searchParams.toString();
	},

	selectShipment: function(idShipment,totalAmount) {
		var data = {};
		data["idShipment"] = idShipment;

		$.ajax({
			headers: {'X-CSRFToken': csrftoken},
			url: "/rest/api/order/shipment/select/",
			type: "post",
			contentType: "application/json",
			data: JSON.stringify(data),

			dataType: "json",
			success: function(jsonResult) {
				$("#shipment-price").html(new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND'}).format(jsonResult.priceShipment));
				$("#payment-price").html(new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND'}).format(jsonResult.priceShipment+totalAmount));

			}
		});
	},

	delete: function(link) {
		var flag = confirm("Bạn có chắc chắn muốn xóa?");
		if (flag == true) {
			location.href = link;
		}
	},

	setPaymentWith: function(value) {
		$('#paymentWith').val(value);
	},
}