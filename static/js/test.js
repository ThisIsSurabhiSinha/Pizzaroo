
// const cartData = localStorage.getItem("cartItems") || '[]'; 
// const container = document.querySelector(".container");
// const table = document.querySelector("table");

// const createTableHeader =()=>{

//         const thead=document.createElement("thead")
//         thead.classList.add("table-primary");

//         const tr=document.createElement("tr");
        
//         const headers= ["Pizza","Size","Crust","Extra Cheese","Quantity"];

//         headers.forEach(headerText=>{
//             const th = document.createElement("th");
//             th.scope = "col";
//             th.classList.add("p-3");
//             th.textContent = headerText;
//             tr.appendChild(th);
            
//         })
//         table.appendChild(thead);
      
// }

// createTableFooter=()=>{
//     <tfoot>
//     <tr>
//       <td colspan="5">Place your order</td>
//     </tr>
//   </tfoot>
//     const tfoot=document.createElement("tfoot");
//     const tr= document.createElement("tr");
//     const td=document.createElement("td");
//     td.colSpan="5";
//     td.innerText="Place your order here";
//     tr.appendChild(td);
//     tfoot.appendChild(tr);
//     table.appendChild(tfoot);

// }

// async function displayCartItems() {
//     if (cartData) {
//         const parsedCartData = JSON.parse(cartData);
//         if (parsedCartData.length === 0) {
//             container.innerHTML = `
//                 <h1>Add items to your cart to place order</h1>
//                 <a class="btn btn-danger" href="/" onclick="window.location.href='/';">Go to home page to select pizza</a>`;
//         } else {
//             console.log("Sending data to server:", parsedCartData); // Log data being sent
//             try {
//                 const response = await fetch("http://127.0.0.1:8000/showCartItems", {
//                     method: "POST",
//                     headers: {
//                         "Content-Type": "application/json",
//                     },
//                     body: JSON.stringify(parsedCartData)
//                 });

//                 if (!response.ok) {
//                     alert("Something went wrong. Try again");
//                 } else {
//                     const data = await response.json();

//                     table.classList.remove("d-none");
          
//                     const tableBody = document.querySelector("table tbody");
//                     tableBody.innerHTML = "";
//                     createTableHeader();
//                     data.forEach((item, i) => {
//                       const row = document.createElement("tr");
                      
                     
                        
                      
//                       row.innerHTML = `
//                                   <td>${item.pizza_name}</td>
//                                   <td>${item.size_name}</td>
//                                   <td>${item.base_name}</td>
//                                   <td>${item.cheese_name }</td>
//                                   <td>
//                                       <div class="p-3" aria-labelledby="customizePizza_${
//                                         item.pizzaId
//                                       }">
//                                           <div class="btn-group">
//                                               <button type="button" class="btn decreaseQuantity no-hover bg-danger text-white" data-pizzaid="${
//                                                 item.pizzaId
//                                               }">
//                                                   <i class="fa-solid fa-minus"></i>
//                                               </button>
//                                               <button type="button" class="btn quantity bg-danger text-white" style="pointer-events: none;">
//                                                   ${item.quantity}
//                                               </button>
//                                               <button type="button" class="btn increaseQuantity no-hover bg-danger-subtle text-white" data-pizzaid="${
//                                                 item.pizzaId
//                                               }">
//                                                   <i class="fa-solid fa-plus"></i>
//                                               </button>
//                                           </div>
//                                       </div>
//                                   </td>
//                               `;
          
//                       tableBody.appendChild(row);

//                       if(i===data.length-1){
//                         createTableFooter();
//                       }
                    
//                     });
//                   }
//                 }
//             }
//              catch (error) {
//                 console.error("Error fetching price:", error);
//             }
//         }
//     }
// }

// document.addEventListener("DOMContentLoaded", displayCartItems);

