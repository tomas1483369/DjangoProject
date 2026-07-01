document.addEventListener('DOMContentLoaded', function () {
    const cartCard = document.querySelector('.items-card[data-api-url]');
    if (!cartCard) {
        return;
    }

    const apiUrl = cartCard.dataset.apiUrl;
    const cartItems = document.getElementById('cart-items');
    const cartTotalAmount = document.getElementById('cart-total-amount');
    const clearCartButton = document.getElementById('clear-cart');
    const cartFooter = document.getElementById('cart-footer-checkout');
    const cartCheckoutPanel = document.getElementById('cart-checkout-panel');
    const cartEmptyState = document.getElementById('cart-empty-state');
    const csrfInput = document.querySelector('#cart-api-form [name=csrfmiddlewaretoken]');

    const getCsrfToken = () => {
        if (csrfInput) {
            return csrfInput.value;
        }
        const name = 'csrftoken';
        const cookies = document.cookie.split(';').map(cookie => cookie.trim());
        const tokenCookie = cookies.find(cookie => cookie.startsWith(`${name}=`));
        return tokenCookie ? decodeURIComponent(tokenCookie.split('=')[1]) : '';
    };

    const fetchCartUpdate = async (formData) => {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCsrfToken(),
            },
            body: formData,
        });

        let data = null;
        try {
            data = await response.json();
        } catch (error) {
            alert('Error en la respuesta del servidor.');
            return null;
        }

        if (!response.ok) {
            alert(data?.message || 'Error en el carrito.');
            return null;
        }

        return data;
    };

    const updateCartState = (data) => {
        if (!data) return;
        cartItems.innerHTML = data.items_html;
        cartTotalAmount.textContent = `$${data.total_amount.toFixed(2)}`;

        if (data.cart_empty) {
            cartFooter?.classList.add('d-none');
            cartCheckoutPanel?.classList.add('d-none');
            cartEmptyState?.classList.remove('d-none');
        } else {
            cartFooter?.classList.remove('d-none');
            cartCheckoutPanel?.classList.remove('d-none');
            cartEmptyState?.classList.add('d-none');
        }
    };

    const handleUpdateAction = async (action, productId, quantity) => {
        const formData = new FormData();
        formData.append('action', action);
        if (productId) {
            formData.append('product_id', productId);
        }
        if (quantity !== undefined) {
            formData.append('quantity', quantity);
        }
        const data = await fetchCartUpdate(formData);
        updateCartState(data);
    };

    cartItems.addEventListener('click', async (event) => {
        const removeButton = event.target.closest('.remove-item');
        const updateButton = event.target.closest('.update-quantity');

        if (removeButton) {
            await handleUpdateAction('remove', removeButton.dataset.productId);
            return;
        }

        if (updateButton) {
            const productId = updateButton.dataset.productId;
            const input = cartItems.querySelector(`.cart-quantity-input[data-product-id="${productId}"]`);
            if (!input) return;

            let quantity = parseInt(input.value, 10) || 1;
            quantity += updateButton.dataset.action === 'increase' ? 1 : -1;
            quantity = Math.max(1, Math.min(quantity, parseInt(input.max, 10) || quantity));
            input.value = quantity;

            await handleUpdateAction('update', productId, quantity);
        }
    });

    cartItems.addEventListener('change', async (event) => {
        const input = event.target.closest('.cart-quantity-input');
        if (!input) return;

        const productId = input.dataset.productId;
        let quantity = parseInt(input.value, 10) || 1;
        quantity = Math.max(1, Math.min(quantity, parseInt(input.max, 10) || quantity));
        input.value = quantity;

        await handleUpdateAction('update', productId, quantity);
    });

    if (clearCartButton) {
        clearCartButton.addEventListener('click', async () => {
            await handleUpdateAction('clear');
        });
    }
});
