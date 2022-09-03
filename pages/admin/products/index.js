import { useRouter } from "next/router";
import { useEffect, useState } from "react";

import { Button } from "antd";
import { DeleteOutlined, EditOutlined } from "@ant-design/icons";

//Import Redux
import { useSelector } from "react-redux";
import { selectIsLoggedIn } from "../../../store/features/userReducer";

import AdminLayout from "../../../layouts/AdminLayout";

function AdminProducts() {
  const router = useRouter();
  const selector = useSelector;
  const isUserLoggedIn = selector(selectIsLoggedIn);

  const deleteHandler = (key) => {
    console.log(`User with id ${key} is deleted!`);
  }

  const editHandler = (key) => {
    console.log(`User with id ${key} is edited!`)
    router.push("/admin/products/"+key);
  }

  //Table Structures
  const [sortedInfo, setSortedInfo] = useState({});

  const tableStructure = [
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
      sorter: (a, b) => a.name.localeCompare(b.name),
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
      sorter: (a, b) => a.category.localeCompare(b.category),
      sortOrder: sortedInfo.columnKey === "category" ? sortedInfo.order : null,
      ellipsis: true,
    },
    {
      title: "Brand",
      dataIndex: "brand",
      key: "brand",
      sorter: (a, b) => a.brand.localeCompare(b.brand),
      sortOrder: sortedInfo.columnKey === "brand" ? sortedInfo.order : null,
      ellipsis: true,
    },
    {
      title: "Condition",
      dataIndex: "condition",
      key: "condition",
      sorter: (a, b) => a.condition.localeCompare(b.condition),
      sortOrder: sortedInfo.columnKey === "condition" ? sortedInfo.order : null,
      ellipsis: true,
    },
    {
      title: "Image",
      dataIndex: "image",
      key: "image",
      render: (record) => <img src={record} style={{ width: '8vw' }} />
    },
    {
      title: "Actions",
      dataIndex: "actions",
      key: "actions",
      render: (_, record) => (
        <>
          <Button type="primary" icon={<EditOutlined />} size={"large"} onClick={() => editHandler(record.key)} />&nbsp;
          <Button type="danger" icon={<DeleteOutlined />} size={"large"} onClick={() => deleteHandler(record.key)} />
        </>
      )
    }
  ];

  const tableData = [
    {
      key: 1,
      name: 'Ipon',
      description: 'ya ipon',
      price: 20000000,
      category: 'Mobile phone',
      brand: 'Apple',
      condition: 'New',
      image: "https://assets.mmsrg.com/isr/166325/c1/-/ASSET_MMS_87346072/fee_786_587_png",
    },
    {
      key: 2,
      name: 'Ipon 11',
      description: 'Ipon terbaru log',
      price: 2000000,
      category: 'Mobile phone',
      brand: 'Apple',
      condition: 'Used',
      image: "https://assets.mmsrg.com/isr/166325/c1/-/ASSET_MMS_87346072/fee_786_587_png",
    },
    {
      key: 3,
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
      slug="products"
      addButton={true}
      showTable={true}
      tableStructure={tableStructure}
      tableData={tableData}
      onSetSortedInfo={setSortedInfo.bind()}
    />
  );
}

export default AdminProducts;
