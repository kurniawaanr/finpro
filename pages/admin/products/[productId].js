import { useRouter } from "next/router";
import { useEffect } from "react";

//Import Redux
import { useSelector } from "react-redux";
import { selectIsLoggedIn } from "../../../store/features/userReducer";

import AdminFormLayout from "../../../layouts/AdminFormLayout";

function AdminProductForm() {
    const router = useRouter();
    const selector = useSelector;
    const isUserLoggedIn = selector(selectIsLoggedIn);

    useEffect(() => {
        if (!isUserLoggedIn) {
            router.push("/adminLogin");
        }
    });

    //console.log(router.query.productId);

    return (
        <AdminFormLayout />
    );
}

export default AdminProductForm;