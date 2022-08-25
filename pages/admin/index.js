import { useRouter } from "next/router";
import { useEffect } from "react";

//Import Redux
import { useSelector } from "react-redux";
import { selectIsLoggedIn } from "../../store/features/userReducer";

import AdminLayout from "../../layouts/AdminLayout";

function AdminHomepage(){
    const router = useRouter();
    const selector = useSelector;
    const isUserLoggedIn = selector(selectIsLoggedIn);

    useEffect(()=>{
        if(!isUserLoggedIn){
            router.push('/login');
        }
    });
    
    return <AdminLayout
        title = "Homepage"
     />;
}

export default AdminHomepage;