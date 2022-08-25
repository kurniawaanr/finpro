import { Fragment } from "react";

import WebsiteHead from "../components/WebsiteHead";
import AdminNavbar from "../components/admins/AdminNavbar";
import AdminMenubar from "../components/admins/AdminMenubar";
import AdminContent from "../components/admins/AdminContent";

function AdminLayout(props) {
  return (
    <Fragment>
      <WebsiteHead
        title="Startup Campus Admin Site"
        desc="Admin system of Startup Campus"
      />

      <AdminNavbar />
      <AdminMenubar />
      <AdminContent {...props} />
    </Fragment>
  );
}

export default AdminLayout;
