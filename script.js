window.onload = () => {
    loadProducts('trending');
    loadCategories();
};

async function loadProducts(type) {
    const container = document.getElementById('products');
    container.innerHTML = '<div class="loading">Loading products...</div>';
    
    let url = '';
    if (type === 'trending') url = '/api/trending';
    else if (type === 'popular') url = '/api/popular';
    else url = '/api/recommendations/P0001';
    
    try {
        const res = await fetch(url);
        const data = await res.json();
        if (data.success) displayProducts(data.data);
        else container.innerHTML = '<div class="loading">No products found</div>';
    } catch(e) {
        console.error(e);
        container.innerHTML = '<div class="loading">Error loading products. Please refresh.</div>';
    }
}

function displayProducts(products) {
    const container = document.getElementById('products');
    if (!products || products.length === 0) {
        container.innerHTML = '<div class="loading">No products found</div>';
        return;
    }
    
    container.innerHTML = products.map(p => `
        <div class="product-card" onclick="alert('Product: ${p.product_name}\\nPrice: ₹${Math.round(p.discounted_price).toLocaleString()}\\nRating: ${p.rating}⭐')">
            <img class="product-img" src="${p.image_url}" onerror="this.src='https://picsum.photos/300/300'" alt="${p.product_name}">
            <div class="product-info">
                <div class="product-cat">${p.product_category}</div>
                <div class="product-name" title="${p.product_name}">${p.product_name}</div>
                <div class="price">
                    <span class="current">₹${Math.round(p.discounted_price).toLocaleString()}</span>
                    ${p.discount_percent > 0 ? `
                        <span class="original">₹${Math.round(p.price).toLocaleString()}</span>
                        <span class="discount">-${p.discount_percent}%</span>
                    ` : ''}
                </div>
                <div class="rating">
                    <div class="stars">${'★'.repeat(Math.floor(p.rating))}${'☆'.repeat(5-Math.floor(p.rating))}</div>
                    <span>${p.rating}</span>
                    <span class="sold">• ${p.quantity_sold.toLocaleString()} sold</span>
                </div>
            </div>
        </div>
    `).join('');
}

async function loadCategories() {
    try {
        const res = await fetch('/api/categories');
        const data = await res.json();
        if (data.success) {
            const container = document.getElementById('categories');
            // Clear existing buttons except "All"
            container.innerHTML = '<button class="cat-btn active" onclick="filterCategory(\'all\')">All</button>';
            
            data.data.forEach(cat => {
                const btn = document.createElement('button');
                btn.className = 'cat-btn';
                btn.textContent = cat;
                btn.onclick = () => filterCategory(cat);
                container.appendChild(btn);
            });
        }
    } catch(e) {
        console.error('Error loading categories:', e);
    }
}

async function filterCategory(cat) {
    // Update active button style
    document.querySelectorAll('.cat-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent === cat || (cat === 'all' && btn.textContent === 'All')) {
            btn.classList.add('active');
        }
    });
    
    if (cat === 'all') {
        loadProducts('trending');
        return;
    }
    
    const container = document.getElementById('products');
    container.innerHTML = '<div class="loading">Loading...</div>';
    
    try {
        const res = await fetch(`/api/category/${encodeURIComponent(cat)}`);
        const data = await res.json();
        if (data.success) displayProducts(data.data);
        else container.innerHTML = '<div class="loading">No products in this category</div>';
    } catch(e) {
        console.error(e);
        container.innerHTML = '<div class="loading">Error loading category</div>';
    }
}

async function searchProducts() {
    const q = document.getElementById('searchInput').value.trim();
    if (q.length < 2) {
        if (q.length === 0) loadProducts('trending');
        return;
    }
    
    const container = document.getElementById('products');
    container.innerHTML = '<div class="loading">Searching...</div>';
    
    try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
        const data = await res.json();
        if (data.success) {
            if (data.data.length === 0) {
                container.innerHTML = '<div class="loading">No products found for "' + q + '"</div>';
            } else {
                displayProducts(data.data);
            }
        }
    } catch(e) {
        console.error(e);
        container.innerHTML = '<div class="loading">Error searching</div>';
    }
}

// Tab active style update
function setActiveTab(btn) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
}

// Make functions global for onclick
window.filterCategory = filterCategory;
window.searchProducts = searchProducts;
window.loadProducts = loadProducts;
window.setActiveTab = setActiveTab;