import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Link from 'next/link';

import { Row, Col, Card, Typography, Pagination, Button, Popover } from "antd";
import { FilterFilled, FunnelPlotFilled } from "@ant-design/icons";

import styled from "styled-components";

import PublicLayout from "../../layouts/PublicLayout";
import CategoryGroup from "../../components/general/CategoryGroup";

const { Title } = Typography;
const { Meta } = Card;

//Styling components
const ProductFilterBox = styled.div`
    width: 20vw;
    float: right;
`;

const SearchWordTitle = styled.p`
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 0;
`;

const SearchWordSubtitle = styled.p`
    font-size: 12px;
    font-weight: 400;
`;

const LeftColumn = styled.div`
  float: left;
`;

const RightColumn = styled.div`
  float: right;
`;

const ProductsShowcase = styled.div`
    clear: both;
`;

const ShowcaseCol = styled(Col)`
    margin-bottom: 2vh;
`;


const PaginationCol = styled(Col)`
    text-align: center;
`;

function ProductPage() {
    //List of Search things
    const [searchWord, setSearchWord] = useState("");
    const [currPage, setCurrPage] = useState(1);
    const [perPage, setPerPage] = useState(50);
    const [sortValue, setSortValue] = useState("nameAsc");

    const [currResult, setCurrResult] = useState(0);
    const [totalResult, setTotalResult] = useState(0);
    const [items, setItems] = useState([]);


    const router = useRouter();

    const categoryExample = [["Category A", "a"], ["Category B", "b"], ["Category C", "c"], ["Category D", "d"]]
    const brandExample = [["Brand A", "a"], ["Brand B", "b"], ["Brand C", "c"], ["Brand D", "d"]]
    const conditionExample = [["New", 0], ["Used", 1]]

    const popoverContent = (
        <div>
            <p><a onClick={() => sortHandler("nameAsc")}>Name Ascending</a></p>
            <p><a onClick={() => sortHandler("nameDesc")}>Name Descending</a></p>
            <p><a onClick={() => sortHandler("priceAsc")}>Price Ascending</a></p>
            <p><a onClick={() => sortHandler("priceDesc")}>Price Descending</a></p>
        </div>
    );

    const formatNumberCurrency = x => {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    useEffect(() => {
        const routerQuery = router.query;

        console.log(routerQuery['search']);
        console.log(routerQuery['perPage']);
        console.log(routerQuery['currPage']);
        console.log(routerQuery['sortOrd']);

        var perPageTemp = currPage;
        var currPageTemp = perPage;

        if (routerQuery['search']) { setSearchWord(decodeURIComponent(routerQuery['search'])) }
        if (routerQuery['perPage']) {
            setPerPage(routerQuery['perPage']);
            perPageTemp = routerQuery['perPage'];
        }
        if (routerQuery['currPage']) {
            setCurrPage(routerQuery['currPage']);
            currPageTemp = routerQuery['currPage']
        }
        if (routerQuery['sortOrd']) { setSortValue(decodeURIComponent(routerQuery['sortOrd'])) }

        setCurrResult(perPageTemp * currPageTemp);
        setTotalResult(1000);

        let productArray = []
        for (let i = 0; i < 10; i++) {
            let product = [];
            product["pId"] = i;
            product["image"] = "https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png";
            product["name"] = decodeURIComponent(routerQuery['search']) + " " + i;
            product["price"] = "Rp " + formatNumberCurrency(500000);
            productArray.push(product);
        }
        setItems(productArray);
    }, [router]);

    const onShowSizeChangeHandler = (currentPage, pageSize) => {
        setPerPage(pageSize);
        setCurrResult(currentPage * pageSize);

        router.query["perPage"] = pageSize;
        router.push(router);
    }

    const onPaginationChangeHandler = (currentPage, pageSize) => {
        setCurrPage(currentPage);
        setCurrResult(currentPage * pageSize);

        router.query["currPage"] = currentPage;
        router.push(router);
    }

    const sortHandler = (sortKey) => {
        setSortValue(sortKey);

        router.query["sortOrd"] = sortKey;
        router.push(router);
    }

    return (
        <PublicLayout title="Product Page">
            <Row gutter={16}>
                <Col span={8}>
                    <ProductFilterBox>
                        <Card title={(<><FilterFilled /> Filter</>)}>
                            <CategoryGroup
                                title="Categories"
                                type="checkbox"
                                options={categoryExample}
                                paramKeyword="cat"
                            />

                            <CategoryGroup
                                title="Brands"
                                type="checkbox"
                                options={brandExample}
                                paramKeyword="brd"
                            />

                            <CategoryGroup
                                title="Prices (in Rp.)"
                                type="slider"
                                maxVal={1000000}
                                paramKeyword="prc"
                            />

                            <CategoryGroup
                                title="Conditions"
                                type="checkbox"
                                options={conditionExample}
                                paramKeyword="cond"
                            />
                        </Card>
                    </ProductFilterBox>
                </Col>
                <Col span={16}>
                    <div>
                        <LeftColumn>
                            <SearchWordTitle>{searchWord}</SearchWordTitle>
                            <SearchWordSubtitle>Search Results {currResult}/{totalResult}</SearchWordSubtitle>
                        </LeftColumn>
                        <RightColumn>
                            <Popover placement="bottomRight" trigger="click" content={popoverContent}>
                                <Button><Title level={5}><FunnelPlotFilled />Sort</Title></Button>
                            </Popover>
                        </RightColumn>
                    </div>
                    <ProductsShowcase>
                        <Row gutter={16}>
                            {items.map(item => {
                                return (
                                    <ShowcaseCol key={item.name} span={8}>
                                        <Link href={`/product/detail/${item.pId}`}>
                                            <Card
                                                hoverable
                                                cover={<img alt={item.name} src={item.image} />}
                                            >
                                                <Meta title={item.name} description={item.price} />
                                            </Card>
                                        </Link>
                                    </ShowcaseCol>
                                );
                            })}
                        </Row>
                    </ProductsShowcase>
                </Col>
                <Col span={8}></Col>
                <PaginationCol span={12}>
                    <Pagination
                        key="productPagination"
                        current={currPage}
                        total={totalResult}
                        pageSize={perPage}
                        onChange={onPaginationChangeHandler}
                        onShowSizeChange={onShowSizeChangeHandler}
                    />
                </PaginationCol>
            </Row>
        </PublicLayout>
    );
}

export default ProductPage;