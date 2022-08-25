import {
  HomeOutlined,
  ShoppingCartOutlined,
  AppstoreOutlined,
  FlagOutlined,
  UserOutlined
} from "@ant-design/icons";

function getItem(label, key, icon, children, type) {
  return {
    key,
    icon,
    children,
    label,
    type,
  };
}

export const menubarItems = [
  getItem("Homepage", "home", <HomeOutlined />),
  getItem("Accounts", "accounts", <UserOutlined />),
  getItem("Banners", "banners", <FlagOutlined />),
  getItem("Products", "products", <ShoppingCartOutlined />,[
    getItem("Products List", "products"),
    getItem("Product Categories","productCategories")
  ]),
  getItem("Partners", "partners", <AppstoreOutlined />,[
    getItem("Partners List", "partners"),
    getItem("Partner Categories","partnerCategories")
  ]),
];