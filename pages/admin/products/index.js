import { useRouter } from "next/router";
import { useEffect, useState } from "react";

//Import Redux
import { useSelector } from "react-redux";
import { selectIsLoggedIn } from "../../../store/features/userReducer";

import AdminLayout from "../../../layouts/AdminLayout";

function AdminProducts() {
  const router = useRouter();
  const selector = useSelector;
  const isUserLoggedIn = selector(selectIsLoggedIn);

  //Table Structures
  const [sortedInfo, setSortedInfo] = useState({});

  const tableStructure = [
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
      sorter: (a, b) => a.name - b.name,
      sortOrder: sortedInfo.columnKey === "name" ? sortedInfo.order : null,
      ellipsis: true,
    },
    {
      title: "Description",
      dataIndex: "description",
      key: "description",
    },
    {
      title: "Price",
      dataIndex: "price",
      key: "price",
      sorter: (a, b) => a.price - b.price,
      sortOrder: sortedInfo.columnKey === "price" ? sortedInfo.order : null,
      ellipsis: true,
    },
    {
      title: "Category",
      dataIndex: "category",
      key: "category",
      sorter: (a, b) => a.category - b.category,
      sortOrder: sortedInfo.columnKey === "category" ? sortedInfo.order : null,
      ellipsis: true,
    },
    {
      title: "Brand",
      dataIndex: "brand",
      key: "brand",
      sorter: (a, b) => a.brand - b.brand,
      sortOrder: sortedInfo.columnKey === "brand" ? sortedInfo.order : null,
      ellipsis: true,
    },
    {
      title: "Condition",
      dataIndex: "condition",
      key: "condition",
      sorter: (a, b) => a.condition - b.condition,
      sortOrder: sortedInfo.columnKey === "condition" ? sortedInfo.order : null,
      ellipsis: true,
    },
    {
      title: "Image",
      dataIndex: "image",
      key: "image",
      render: (record) => <img src={record} style={{width:'8vw'}} />
    },
  ];

  const tableData = [
      {
          name: 'Ipon',
          description: 'ya ipon',
          price: 20000000,
          category: 'Mobile phone',
          brand: 'Apple',
          condition: 'New',
          image: "https://assets.mmsrg.com/isr/166325/c1/-/ASSET_MMS_87346072/fee_786_587_png",
      },
      {
        name: 'Nokia',
        description: 'ya nokia',
        price: 1000,
        category: 'Mobile phone',
        brand: 'Nokia',
        condition: 'Used',
        image: "https://manual-user-guide.com/images/phones/nokia_6630.png",
    }
  ]

  useEffect(() => {
    if (!isUserLoggedIn) {
      router.push("/login");
    }
  });

  return (
    <AdminLayout
      title="Products"
      singleWord="Product"
      addButton={true}
      showTable={true}
      tableStructure={tableStructure}
      tableData={tableData}
      onSetSortedInfo={setSortedInfo.bind()}
    />
  );
}

export default AdminProducts;
