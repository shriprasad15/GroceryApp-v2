export async function fetchCategories() {
      try {
        const response = await fetch('http://127.0.0.1:5003/api/category');

        const data = await response.json();
        if (!response.ok) {
          throw data;
        }
        return data
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    }
export async function fetchPendingCategories() {
  try {
    const response = await fetch('http://127.0.0.1:5003/api/pending-category',{
      method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
        }
    });
    const data = await response.json();
    if (!response.ok) {

      throw data;
    }

    return data
  } catch (error) {
    console.error('Error fetching categories:', error);
  }
}

export async function fetchProducts() {
      try {
        const response = await fetch('http://127.0.0.1:5003/api/products');
        const data = await response.json();
        // console.log(data)
        if (response.ok) {
          return data;
        } else {
          console.error('Failed to fetch products');
        }
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    }


export async function fetchProductsByCategory(item_id) {
  try {
    const response = await fetch(`http://127.0.0.1:5003/api/product/cat/${item_id}`);
    const data = await response.json();
    // console.log(data)
    if (response.ok) {
      return data;
    } else {
      console.error('Failed to fetch products');
    }
  } catch (error) {
    console.error('Error fetching products:', error);
  }
}

export async function deleteProductById(itemId) {
  try {
    const response = await fetch(`http://127.0.0.1:5003/api/product/${itemId}`, {
      method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
        }
    });

    if (response.ok) {
      return response
    } else {
      const errorData = await response.json();
      throw new Error(`Failed to delete product. ${errorData.message}`);
    }
  } catch (error) {
    return { success: false, message: `Error deleting product: ${error.message}` };
  }
}

export async function updateProduct(productId, productData) {
  try {
    const response = await fetch(`http://127.0.0.1:5003/api/product/${productId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
          'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))

      },
      body: JSON.stringify(productData),
    });
    return {
      ok: response.ok,
      data: await response.json(),
    };
  } catch (error) {
    console.error('Error updating product:', error);
    throw error;
  }
}

export async function fetchPendingManagers() {
      try {
        const response = await fetch('http://127.0.0.1:5003/api/pending-managers',{
            method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
                }
            });


        const data = await response.json();
        if (!response.ok) {
          throw data;
        }
        return data
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    }

    export async function installApp(){
      // try {
      //   const response = await fetch("http://127.0.0.1:5003/add-to-desktop", {
      //     method: "POST",
      //     headers: {
      //       "Content-Type": "application/json",
      //     },
      //     body: JSON.stringify({
      //       "name": "GroceryApp",
      //       "url": "http://localhost:8080/",
      //       "icon": "https://cdn.iconscout.com/icon/free/png-256/grocery-185-461761.png"
      //     }),
      //   });
      //   if (response.ok) {
      //     alert("Grocery App Added to Desktop")
      //     // Handle success: show a message, update UI, etc.
      //   } else {
      //     console.error("Failed to create shortcut");
      //     // Handle failure: show an error message, retry logic, etc.
      //   }
      // } catch (err) {
      //   console.error(err);
      //   // Handle exceptions here
      // }


      if (navigator.installManifest) {
        navigator.installManifest('/manifest.json')
          .then(() => console.log('App installed successfully!'))
          .catch(error => console.error('Error installing app:', error));
      } else {
        console.warn('Install prompt not available.');
      }



}

    export async function fetchProfileDetails() {
      try {
        const response = await fetch('http://127.0.0.1:5003/api/buy',{
            method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
                }
            });
        const data = await response.json();
        if (!response.ok) {
          throw data;
        }
        console.log("data",data)
        return data
        }
        catch (error) {
        console.error('Error fetching categories:', error);
        }
    }