"use client";

import { setAuth, setLogout } from '@/lib/redux/features/auth/authSlice';
import { useAppDispatch } from '@/lib/redux/hooks/typedHooks';
import {getCookie} from "cookies-next";
import {useEffect} from 'react';

export default function PersistAuth() {
    const dispatch = useAppDispatch();
    useEffect(()=>{
        const isLoggedIn = getCookie("logged_in")==="true"
        if (isLoggedIn) {
            dispatch(setAuth())
        }else{
            dispatch(setLogout())
        }
    },[dispatch]);
  return null
}
