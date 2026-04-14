import { initializeApp } from "https://gstatic.com";
import { getAuth, signInWithEmailAndPassword, GoogleAuthProvider, signInWithPopup, onAuthStateChanged, signOut } from "https://gstatic.com";
import { getFirestore, doc, getDoc, setDoc, updateDoc, collection, addDoc, onSnapshot, query, where } from "https://gstatic.com";

const firebaseConfig = {
    apiKey: "AIzaSyAVEwTJEHFRnGnbl4wuTTPzRBDVTFBDtrg",
    authDomain: "://firebaseapp.com",
    projectId: "coding-shop"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// Services Data
const services = [
    { name: 'WhatsApp', price: 0.50, icon: 'https://icons8.com' },
    { name: 'Instagram', price: 0.30, icon: 'https://icons8.com' },
    { name: 'Facebook', price: 0.25, icon: 'https://icons8.com' },
    { name: 'Google', price: 0.60, icon: 'https://icons8.com' }
];

// --- AUTHENTICATION ---
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').onsubmit = async (e) => {
        e.preventDefault();
        try {
            await signInWithEmailAndPassword(auth, email.value, password.value);
            window.location.href = "dashboard.html";
        } catch (err) { alert(err.message); }
    };

    document.getElementById('googleLogin').onclick = async () => {
        const provider = new GoogleAuthProvider();
        const result = await signInWithPopup(auth, provider);
        await setDoc(doc(db, "users", result.user.uid), { balance: 0, email: result.user.email }, { merge: true });
        window.location.href = "dashboard.html";
    };
}

// --- DASHBOARD LOGIC ---
onAuthStateChanged(auth, async (user) => {
    if (user) {
        if (window.location.pathname.includes("dashboard.html")) {
            // Update UI with Balance
            onSnapshot(doc(db, "users", user.uid), (doc) => {
                document.getElementById('userBalance').innerText = `$${doc.data()?.balance.toFixed(2)}`;
            });
            renderServices();
        }
        // Admin Redirect check
        if (window.location.pathname.includes("admin.html") && user.email !== "admin@gmail.com") {
            window.location.href = "dashboard.html";
        }
    }
});

function renderServices() {
    const grid = document.getElementById('servicesGrid');
    if (!grid) return;
    grid.innerHTML = services.map(s => `
        <div class="col-md-3 col-6">
            <div class="premium-card text-center p-4" onclick="openBuyModal('${s.name}', ${s.price})">
                <img src="${s.icon}" class="service-icon">
                <h6>${s.name}</h6>
                <span class="text-primary">$${s.price}</span>
            </div>
        </div>
    `).join('');
}

// --- RAZORPAY PAYMENT ---
if (document.getElementById('addMoneyBtn')) {
    document.getElementById('addMoneyBtn').onclick = () => {
        const amt = document.getElementById('rechargeAmount').value;
        const options = {
            key: "rzp_test_xxxxx",
            amount: amt * 100,
            currency: "USD",
            name: "EliteSMS",
            handler: async (res) => {
                const userRef = doc(db, "users", auth.currentUser.uid);
                const current = (await getDoc(userRef)).data().balance;
                await updateDoc(userRef, { balance: current + parseFloat(amt) });
                alert("Payment Successful!");
            }
        };
        const rzp = new Razorpay(options);
        rzp.open();
    };
}

// --- ORDERING LOGIC ---
let selectedService = {};
window.openBuyModal = (name, price) => {
    selectedService = { name, price };
    document.getElementById('modalTitle').innerText = `Buy ${name}`;
    document.getElementById('modalPrice').innerText = `$${price}`;
    new bootstrap.Modal(document.getElementById('buyModal')).show();
};

document.getElementById('confirmPurchase')?.addEventListener('click', async () => {
    const qty = document.getElementById('qtyInput').value;
    const userRef = doc(db, "users", auth.currentUser.uid);
    const balance = (await getDoc(userRef)).data().balance;
    const total = selectedService.price * qty;

    if (balance >= total) {
        await addDoc(collection(db, "orders"), {
            uid: auth.currentUser.uid,
            email: auth.currentUser.email,
            service: selectedService.name,
            qty: qty,
            country: document.getElementById('countrySelect').value,
            status: 'pending',
            date: new Date()
        });
        await updateDoc(userRef, { balance: balance - total });
        alert("Order Placed!");
        location.reload();
    } else {
        alert("Insufficient Balance!");
    }
});
