import React, { createContext, useState, useEffect, useContext } from 'react';
import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signInWithPopup,
    signOut,
    onAuthStateChanged
} from 'firebase/auth';
import { auth, googleProvider } from '../firebase';

const AuthContext = createContext();

export function useAuth() {
    return useContext(AuthContext);
}

export function AuthProvider({ children }) {
    const [currentUser, setCurrentUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Signup with email and password
    function signup(email, password) {
        return createUserWithEmailAndPassword(auth, email, password);
    }

    // Login with email and password
    function login(email, password) {
        return signInWithEmailAndPassword(auth, email, password);
    }

    // Login with Google
    function loginWithGoogle() {
        return signInWithPopup(auth, googleProvider);
    }

    // Logout
    function logout() {
        return signOut(auth);
    }

    // Get current user's ID token
    async function getIdToken() {
        if (currentUser) {
            return await currentUser.getIdToken();
        }
        return null;
    }

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (user) => {
            setCurrentUser(user);
            setLoading(false);
        });

        return unsubscribe;
    }, []);

    const value = {
        currentUser,
        signup,
        login,
        loginWithGoogle,
        logout,
        getIdToken
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
}
