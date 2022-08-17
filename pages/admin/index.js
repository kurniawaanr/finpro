import { useRouter } from "next/router";
import { useEffect } from "react";

//Import Redux
import { useDispatch, useSelector } from "react-redux";
import { logoutHandler, selectIsLoggedIn } from "../../store/features/userReducer";

function AdminHomepage(){
    // const dispatch = useDispatch();
    // dispatch(logoutHandler());

    const router = useRouter();
    const selector = useSelector;
    const isUserLoggedIn = selector(selectIsLoggedIn);

    console.log(isUserLoggedIn);
    useEffect(()=>{
        if(!isUserLoggedIn){
            router.push('/login');
        }
    });
    
    return <h1>Admin Page</h1>
}

export default AdminHomepage;