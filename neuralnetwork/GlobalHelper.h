#pragma once


#include <Eigen/Core>

#include <iostream>

//general class with helper functions to be used throughout.
//includes some function templates translating Python-Numpy methods into c++/Eigen.

using namespace Eigen;


template<class ArgType, class ColIndexType>
class indexing_functor {
    const ArgType& m_arg;
    //const RowIndexType& m_rowIndices;
    const ColIndexType& m_colIndices;
public:
    typedef Eigen::Array<typename ArgType::Scalar,
        ColIndexType::SizeAtCompileTime,
        1,
        ArgType::Flags& Eigen::RowMajorBit ? Eigen::RowMajor : Eigen::ColMajor,
        ColIndexType::MaxSizeAtCompileTime,
        1> ArrayType;

    indexing_functor(const ArgType& arg, const ColIndexType& col_indices)
        : m_arg(arg), m_colIndices(col_indices)
    {}

    const typename ArgType::Scalar& operator() (Eigen::Index row, Eigen::Index col) const {
        //std::cout << "in functor " << col << std::endl;
        return m_arg(row, m_colIndices[row]);
    }
};


template<class ArgType, class ColIndexType>
Eigen::CwiseNullaryOp<indexing_functor<ArgType, ColIndexType>, typename indexing_functor<ArgType, ColIndexType>::ArrayType>
arrayColumnIndices(const Eigen::ArrayBase<ArgType>& arg, const ColIndexType& colIndices) {
    typedef indexing_functor<ArgType, ColIndexType> Func;
    typedef typename Func::ArrayType ArrayType;
    //std::cout << "in nullary functor " << colIndices << std::endl;
    return ArrayType::NullaryExpr(colIndices.size(), 1, Func(arg.derived(), colIndices));
}


template<class ArgType>
class newarray_functor {
    const ArgType& m_zeroarr;
    const ArgType& m_transformrow;   
public:
    typedef Eigen::Array<typename ArgType::Scalar,
        ArgType::SizeAtCompileTime,
        ArgType::SizeAtCompileTime,
        ArgType::Flags& Eigen::RowMajorBit ? Eigen::RowMajor : Eigen::ColMajor,
        ArgType::SizeAtCompileTime,
        ArgType::SizeAtCompileTime> ArrayType;
    /*
    typedef Eigen::Array<typename ArgType1::Scalar,
        ArgType1::SizeAtCompileTime,
        ArgTypee::SizeAtCompileTime,
        ArgType::Flags& Eigen::RowMajorBit ? Eigen::RowMajor : Eigen::ColMajor,
        ArgTypee::SizeAtCompileTime,
        ArgTypee::SizeAtCompileTime> ArrayType;
        */
    newarray_functor(const ArgType& zeroarr, const ArgType& transformrow)
        : m_zeroarr(zeroarr), m_transformrow(transformrow)
    {}

    const typename ArgType::Scalar& operator() (Eigen::Index row, Eigen::Index col) const {
        //std::cout << "in functor " << row << std::endl;
        if (row == col) {
            return m_transformrow(row);
        }
        else {
            return m_zeroarr(row, col);
        }       
    }
};


template<class ArgType>
Eigen::CwiseNullaryOp<newarray_functor<ArgType>, typename newarray_functor<ArgType>::ArrayType>
rowIdentity(const Eigen::ArrayBase<ArgType>& zeroarr, const Eigen::ArrayBase<ArgType>& transformrow) {
    typedef newarray_functor<ArgType> Func;
    typedef typename Func::ArrayType ArrayType;
    return ArrayType::NullaryExpr(zeroarr.rows(), zeroarr.cols(), Func(zeroarr.derived(), transformrow.derived()));
}


template<class ArgType, class ColIndexType>
class hotencoding_functor {
    const ArgType& m_zeroarr;
    const ColIndexType& m_indices;
public:
    typedef Eigen::Array<typename ArgType::Scalar,
        ArgType::SizeAtCompileTime,
        ArgType::SizeAtCompileTime,
        ArgType::Flags& Eigen::RowMajorBit ? Eigen::RowMajor : Eigen::ColMajor,
        ArgType::SizeAtCompileTime,
        ArgType::SizeAtCompileTime> ArrayType;
    
    hotencoding_functor(const ArgType& zeroarr, const ColIndexType& transformrow)
        : m_zeroarr(zeroarr), m_indices(transformrow)
    {}

    const typename ArgType::Scalar& operator() (Eigen::Index row, Eigen::Index col) const {
        //std::cout << "in functor " << row << std::endl;
        if (col == m_indices[row]) {
            return 1;
       }
        else {
            return m_zeroarr(row, col);
        }
    }
};


template<class ArgType, class ColIndexType>
Eigen::CwiseNullaryOp<hotencoding_functor<ArgType, ColIndexType>, typename hotencoding_functor<ArgType, ColIndexType>::ArrayType>
hotEncode(const Eigen::ArrayBase<ArgType>& zeroarr, const ColIndexType& transformrow) {
    typedef hotencoding_functor<ArgType, ColIndexType> Func;
    typedef typename Func::ArrayType ArrayType;
    return ArrayType::NullaryExpr(zeroarr.rows(), zeroarr.cols(), Func(zeroarr.derived(), transformrow.derived()));
}


template<class ArgType>
class argmax_functor {
    const ArgType& m_mainarr;
    int axis;
public:
    typedef Eigen::Array<typename ArgType::Scalar,
        ArgType::SizeAtCompileTime,
        ArgType::SizeAtCompileTime,
        ArgType::Flags& Eigen::RowMajorBit ? Eigen::RowMajor : Eigen::ColMajor,
        ArgType::SizeAtCompileTime,
        ArgType::SizeAtCompileTime> ArrayType;

    argmax_functor(const ArgType& mainarr, int axisIn)
        : m_mainarr(mainarr), axis(axisIn)
    {}

    const typename ArgType::Scalar& operator() (Eigen::Index row, Eigen::Index col) const {
        
        Index maxRow, maxCol;
        if (axis == 0) {
            m_mainarr.row(row).maxCoeff(&maxRow, &maxCol);
            return maxCol;
        }
        else {
            m_mainarr.col(col).maxCoeff(&maxRow, &maxCol);
            return maxRow;
        }
                
    }
};

template<class ArgType>
Eigen::CwiseNullaryOp<argmax_functor<ArgType>, typename argmax_functor<ArgType>::ArrayType>
argmax(const Eigen::ArrayBase<ArgType>& mainarr, int axis) {
    typedef argmax_functor<ArgType> Func;
    typedef typename Func::ArrayType ArrayType;
    if (axis == 0) {
        return ArrayType::NullaryExpr(mainarr.rows(), 1, Func(mainarr.derived(), axis));
    }
    else {
        return ArrayType::NullaryExpr(1, mainarr.cols(), Func(mainarr.derived(), axis));
    }
}

class GlobalHelper {
public:
	GlobalHelper();
	float getRandomFloat(int min, int max);
    float accuracy(ArrayXXf softmaxOut, ArrayXi classes);
   
	

};
