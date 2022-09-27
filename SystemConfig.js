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

//Misc
export const shippingMethods = [
  {name: "same day", price: 100000},
  {name: "tomorrow", price: 50000},
  {name: "next time", price: 0},
];

//MENU
export const menubarItems = [
  getItem("Homepage", "home", <HomeOutlined />),
  getItem("Accounts", "accounts", <UserOutlined />),
  getItem("Banners", "banners", <FlagOutlined />),
  getItem("Products", "products", <ShoppingCartOutlined />, [
    getItem("Products List", "products"),
    getItem("Product Categories", "productCategories")
  ]),
  getItem("Partners", "partners", <AppstoreOutlined />, [
    getItem("Partners List", "partners"),
    getItem("Partner Categories", "partnerCategories")
  ]),
];

export const profileMenuItems = [
  getItem("My Account", "myAccount"),
  getItem("My Orders", "myOrders"),
  getItem("Order Track", "orderTrack"),
  getItem("Wishlist", "wishlist"),
]

//FORM
export const productFormStructure = [
  ["Name", "name", "text", [
    {
      required: true,
      message: 'Please input product name!',
    },
  ]],
  ["Description", "description", "multilineText", "none"],
  ["Price", "price", "number", [
    {
      required: true,
      message: 'Please input product price!',
    }
  ]],
  ["Category", "category", "selectBox", [
    {
      required: true,
      message: 'Please choose products category!',
    },
  ], ["Pakaian Pria", "Pakaian Wanita", "Pakaian Anak"]],
  ["Brand", "brand", "selectBox", [
    {
      required: true,
      message: 'Please choose products brand!',
    },
  ], ["Boss", "Gucci", "Fossil"]],
  ["Condition", "condition", "selectBox", [
    {
      required: true,
      message: 'Please choose products condition!',
    },
  ], ["New", "Used"]],
  ["Image", "image", "uploadImage", [
    {
      required: true,
      message: 'Please input product image!',
    },
  ]]
];

export const shippingFormStructure = [
  ["Name", "name", "text", [
    {
      required: true,
      message: 'Please input shipping name!',
    },
  ]],
  ["Phone", "phone", "text", [
    {
      required: true,
      message: 'Please input shipping phone!',
    },
  ]],
  ["Address", "address", "multilineText", [
    {
      required: true,
      message: 'Please input shipping address!',
    },
  ]],
]