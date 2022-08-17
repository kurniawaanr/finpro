import { Fragment } from "react";

import WebsiteHead from "../components/WebsiteHead";
import AdminNavbar from "../components/admins/AdminNavbar";
import AdminMenubar from "../components/admins/AdminMenubar";

function AdminLayout() {
  return (
    <Fragment>
      <WebsiteHead
        title="Startup Campus Admin Site"
        desc="Admin system of Startup Campus"
      />

      <AdminNavbar />
      <AdminMenubar />
    </Fragment>
  );
}

export default AdminLayout;
