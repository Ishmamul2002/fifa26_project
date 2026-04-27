function addToCart(ticketType, price) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart.push({
        type: ticketType,
        price: price,
        details: "Mexico vs South Korea - June 11, 2026"
    });
    localStorage.setItem('cart', JSON.stringify(cart));
    alert(`✅ Added to Cart: ${ticketType} - $${price}`);
}