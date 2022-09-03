import { Fragment } from "react";

import WebsiteHead from "../components/WebsiteHead";
import AdminNavbar from "../components/admins/AdminNavbar";
import AdminMenubar from "../components/admins/AdminMenubar";
import AdminFormContent from "../components/admins/AdminFormContent";

function AdminFormLayout(props) {
    return (
        <Fragment>
            <WebsiteHead
                title="Startup Campus Admin Site"
                desc="Admin system of Startup Campus"
            />
            <AdminNavbar />
            <AdminMenubar />
            <AdminFormContent />
        </Fragment>
    );
}

export default AdminFormLayout;