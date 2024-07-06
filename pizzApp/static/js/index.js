
const update_number_of_items_in_cart = () => {
  let cartData = JSON.parse(localStorage.getItem("cartItems")) || [];
  let totalItems = 0;
  let totalCost = 0;

  if (cartData.length) {
      for (const item of cartData) {
          totalItems += parseInt(item.quantity);
          totalCost += parseFloat(item.quantity * item.price); // Assuming 'price' is in the item
      }

      let showItems = document.querySelector(".showItem");
      showItems.innerText = totalItems;
  }
};

const decreaseQuantity = (e) => {
  let quantity_section = e.target.closest(".btn-group").querySelector(".quantity");

  if (quantity_section) {
      let curr_quantity = parseInt(quantity_section.innerText);

      if (curr_quantity > 0) {
          quantity_section.innerText = curr_quantity - 1;
          updatePrice(e);
      }
  } else {
      console.error("Quantity section not found");
  }
};

const increaseQuantity = (e) => {
  let quantity_section = e.target.closest(".btn-group").querySelector(".quantity");

  if (quantity_section) {
      let curr_quantity = parseInt(quantity_section.innerText);

      if (curr_quantity < 10) {
          quantity_section.innerText = curr_quantity + 1;
          updatePrice(e);
      }
  } else {
      console.error("Quantity section not found");
  }
};

const updatePrice = async (e) => {
  
  const URL_FOR_PRICE_UPDATE = "https://pizzaroo-pizza-delivery-app.onrender.com/calculatePrice";
  const form = e.target.closest(".customiziationForm");
  //form.preventDefault();
  if (!form) {
      console.error("Form not found");
      return;
  }

  const pizzaId = form.dataset.pizzaid;
  const baseId = form.querySelector('input[name^="crust_"]:checked').value;
  const sizeId = form.querySelector('input[name^="size"]:checked').value;
  const cheeseId = form.querySelector('input[name^="cheese"]:checked').value;

  const data = {
      baseId,
      cheeseId,
      sizeId,
      pizzaId,
  };

  try {
      const response = await fetch(URL_FOR_PRICE_UPDATE, {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
      });

      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }

      const priceData = await response.json();
      let curr_quantity = 1;
      let quantity_section = form.querySelector(".quantity");
      if (quantity_section) {
          let quantity = parseInt(quantity_section.innerText);
          if (quantity > 0) curr_quantity = quantity;
      } else {
          console.error("Quantity section not found");
      }

      const total_price = (parseInt(curr_quantity) * parseFloat(priceData.price)).toFixed(2);
      let showPriceElement = form.querySelector(`.showPrice_${pizzaId}`);

      if (showPriceElement) {
          showPriceElement.innerText = total_price;
      } else {
          console.error("Show price element not found");
      }
  } catch (error) {
      console.error("Error fetching price:", error);
  }
};

function addToCart(event) {
  const pizzaId = event.target.dataset.pizzaid;

  const form = document.querySelector(`.customiziationForm[data-pizzaid="${pizzaId}"]`);
  if (form) {
      const baseId = form.querySelector('input[name^="crust_"]:checked').value;
      const sizeId = form.querySelector('input[name^="size"]:checked').value;
      const cheeseId = form.querySelector('input[name^="cheese"]:checked').value;
      const quantity = parseInt(form.querySelector(".quantity").innerText);
      const minPrice=parseFloat(form.querySelector(".minPrice").innerText);

      let cartData = JSON.parse(localStorage.getItem("cartItems")) || [];

      const cartItem = {
          pizzaId,
          baseId,
          sizeId,
          cheeseId,
          quantity,
          price: parseFloat(form.querySelector(`.showPrice_${pizzaId}`).innerText),
          minPrice
      };

      const existingItem = cartData.find(item => item.pizzaId === pizzaId);

      if (existingItem) {
          existingItem.quantity += quantity;
      } else {
          cartData.push(cartItem);
      }

      localStorage.setItem("cartItems", JSON.stringify(cartData));

      form.reset();
      form.querySelector(`.showPrice_${pizzaId}`).innerHTML=minPrice.toFixed(2);
      form.querySelector(".quantity").innerText="1";
      update_number_of_items_in_cart();
  } else {
      console.error("Form not found");
  }
}

document.addEventListener("DOMContentLoaded", (event) => {

  const allForms = document.querySelectorAll(".customiziationForm");
  const allMinusBtn = document.querySelectorAll(".decreaseQuantity");
  const allPlusBtn = document.querySelectorAll(".increaseQuantity");
  const allAddBtn = document.querySelectorAll(".addBtn");
  
  
  update_number_of_items_in_cart();

  allForms.forEach((current_form) => {
      current_form.addEventListener("change", updatePrice);
  });

  allMinusBtn.forEach((curr_minus_btn) => {
      curr_minus_btn.addEventListener("click", decreaseQuantity);
  });

  allPlusBtn.forEach((curr_plus_btn) => {
      curr_plus_btn.addEventListener("click", increaseQuantity);
  });

  allAddBtn.forEach((curr_add_btn) => {
      curr_add_btn.addEventListener("click", addToCart);
  });
});

