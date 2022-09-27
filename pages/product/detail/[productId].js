import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/router";

import { Row, Col, Carousel, Typography, Button, InputNumber, Divider } from "antd";
import { HeartOutlined, ShareAltOutlined, HeartFilled } from "@ant-design/icons";
const { Title, Text } = Typography;
import styled from "styled-components";

//Use Redux
import { useDispatch, useSelector } from "react-redux";
import { wishlistItems, addItemWishlistHandler, removeItemWishlistHandler } from "../../../store/features/wishlistReducer";
import { addChangeItemCartHandler } from "../../../store/features/cartReducer";

import PublicLayout from "../../../layouts/PublicLayout";

//Styling components
const ProductDetailPicture = styled.img`
    width: 20vw;
`;

const ProductDetailCarousel = styled.div`
    width: 20vw;
    float: right;
`;

const ItemSizeRadio = styled(Button)`
    margin: 0 0.25vw;
    border-radius: 5px;
`;

const ProductDetailBox = styled.div`
    padding-left: 3vw;
    padding-top: 1vh;
`;

const ProductDetailDivider = styled(Divider)`
    width: 15vw;
    min-width: 15vw;
`;

const SPSlideShow = styled.div`
    padding: 1vw;
`;

const SPImage = styled.img`
    width: 100%;
    height: 100%;
    border: 1px solid lightgray;
`;

function DetailProductPage() {
    const dispatch = useDispatch();
    const selector = useSelector;
    const wishlistArr = selector(wishlistItems);

    const [productName, setProductName] = useState('');
    const [brandName, setBrandName] = useState('');
    const [price, setPrice] = useState('');
    const [productDetail, setProductDetail] = useState('');
    const [faves, setFaves] = useState();
    const [itemSize, setItemSize] = useState("s");
    const qtyInput = useRef(1);

    const router = useRouter();
    //console.log(router.query.productId);

    useEffect(() => {
        setProductName("Navy Club Tas Selempang Travel Cross Body Bag GGH - Sling bag - Hitam");
        setBrandName("Tokopedia");
        setPrice("Rp119.000");
        setProductDetail("Navy Club Tas Selempang Punggung berbahan polyester cocok untuk Anda yang sering beraktifitas diluar ruangan/outdoor. Pada kolom utama dilengkapi dengan sekat tablet dan kaitan untuk gantungan kunci. Tersedia kolom tambahan dibagian depan tas untuk menyimpan barang yang sering diakses.");

        setFaves(wishlistArr.includes(router.query.productId))
    });

    const AddWishlistHandler = () => {
        setFaves(true);
        dispatch(addItemWishlistHandler({itemId: router.query.productId}));
    }
    const RemoveWishlistHandler = () => {
        setFaves(false);
        dispatch(removeItemWishlistHandler({itemId: router.query.productId}));
    }

    const AddCartHandler = () => {
        //console.log("test");
        //console.log(qtyInput.current.value);
        //console.log(itemSize);
        dispatch(addChangeItemCartHandler({itemId: router.query.productId, size: itemSize, qty: qtyInput.current.value, type: "add"}));
    }

    return (
        <PublicLayout title="Detail Product Page">
            <Row gutter={16}>
                <Col className="gutter-row" span={8}>
                    <ProductDetailCarousel>
                        <Carousel autoplay>
                            <div>
                                <ProductDetailPicture src="https://images.tokopedia.net/img/cache/700/VqbcmM/2022/6/4/d1ce779e-adaf-4449-bd52-d91f73dcc23c.jpg.webp?ect=4g" />
                            </div>
                            <div>
                                <ProductDetailPicture src="https://images.tokopedia.net/img/cache/500-square/VqbcmM/2022/6/4/ce9acd9b-1453-4d94-9a03-1e47810da655.jpg.webp?ect=4g" />
                            </div>
                            <div>
                                <ProductDetailPicture src="https://images.tokopedia.net/img/cache/700/VqbcmM/2022/6/4/bc460c58-a5c7-4fe1-8dd4-579c476f8097.jpg.webp?ect=4g" />
                            </div>
                            <div>
                                <ProductDetailPicture src="https://images.tokopedia.net/img/cache/100-square/VqbcmM/2022/6/4/bc460c58-a5c7-4fe1-8dd4-579c476f8097.jpg.webp?ect=4g" />
                            </div>
                        </Carousel>
                    </ProductDetailCarousel>
                </Col>
                <Col className="gutter-row" span={12}>
                    <Title level={2}>{productName}</Title>
                    <br />
                    <Text type="secondary">{brandName}</Text>
                    <br />
                    <Title level={4}>{price}</Title>
                    Size &nbsp;
                    <ItemSizeRadio onClick={(e)=>setItemSize("s")}>S</ItemSizeRadio>
                    <ItemSizeRadio onClick={(e)=>setItemSize("m")}>M</ItemSizeRadio>
                    <ItemSizeRadio onClick={(e)=>setItemSize("l")}>L</ItemSizeRadio>
                    <ItemSizeRadio onClick={(e)=>setItemSize("xl")}>XL</ItemSizeRadio>
                    <br /><br />
                    Qty &nbsp; <InputNumber ref={qtyInput} />
                    <br/><br />
                    <Button type="primary" onClick={AddCartHandler}>Add to cart</Button> &nbsp; {!faves && <HeartOutlined onClick={AddWishlistHandler} style={{fontSize: "25px"}} />}{faves && <HeartFilled onClick={RemoveWishlistHandler} style={{fontSize: "25px"}} />} &nbsp; <ShareAltOutlined style={{fontSize: "25px"}} />
                </Col>
            </Row>
            <ProductDetailBox>
                <Title level={3}>Product Detail</Title>
                <ProductDetailDivider />
                <p>{productDetail}</p>
            </ProductDetailBox>
            <ProductDetailBox>
                <Title level={3}>Similar Products</Title>
                <ProductDetailDivider />
                <Carousel autoplay slidesToShow={5}>
                    <SPSlideShow>
                        <SPImage src="https://s1.bukalapak.com/img/11556714892/s-246-246/data.jpeg.webp" />
                    </SPSlideShow>
                    <SPSlideShow>
                        <SPImage src="https://s2.bukalapak.com/img/23991616792/s-246-246/data.jpeg.webp" />
                    </SPSlideShow>
                    <SPSlideShow>
                        <SPImage src="https://s2.bukalapak.com/img/25081499692/s-246-246/data.jpeg.webp" />
                    </SPSlideShow>
                    <SPSlideShow>
                        <SPImage src="https://s2.bukalapak.com/img/79689041572/s-246-246/data.jpeg.webp" />
                    </SPSlideShow>
                    <SPSlideShow>
                        <SPImage src="https://s0.bukalapak.com/img/58914080992/s-246-246/data.jpeg.webp" />
                    </SPSlideShow>
                    <SPSlideShow>
                        <SPImage src="https://s1.bukalapak.com/img/66099775371/s-246-246/data.jpeg.webp" />
                    </SPSlideShow>
                </Carousel>
            </ProductDetailBox>


        </PublicLayout>
    );
}

export default DetailProductPage;