#pragma once
#include "DWrap.h"


Napi::FunctionReference DWrap::constructor;

Napi::Object DWrap::Init(Napi::Env env, Napi::Object exports) {
	Napi::HandleScope scope(env);
	Napi::Function func = DefineClass(env, "DWrap", {
		InstanceMethod("loadParams", &DWrap::loadParams),
		InstanceMethod("getCfg", &DWrap::getCfg),
		InstanceMethod("getX", &DWrap::getX),
		InstanceMethod("getY", &DWrap::getY),
		InstanceMethod("detect", &DWrap::detect),
		});

	constructor = Napi::Persistent(func);
	constructor.SuppressDestruct();

	exports.Set("DWrap", func);
	return exports;
}


DWrap::DWrap(const Napi::CallbackInfo& info) : Napi::ObjectWrap<DWrap>(info) {
	Napi::Env env = info.Env();
	Napi::HandleScope scope(env);

	int length = info.Length();

	if (length > 0) {
		Napi::TypeError::New(env, "Instancing net " + std::to_string(length)).ThrowAsJavaScriptException();
	}

	this->_dnet = new DNet();
	return;
}

void DWrap::loadParams(const Napi::CallbackInfo& info) {
	Napi::Env env = info.Env();
	Napi::HandleScope scope(env);

	if (info.Length() < 2) {
		Napi::TypeError::New(env, "Too few arguments").ThrowAsJavaScriptException();

	}

	Napi::String cfg = info[0].As<Napi::String>();
	Napi::String weights = info[1].As<Napi::String>();
	try {
		this->_dnet->setParams(cfg.ToString(), weights.ToString());
	}
	catch (Napi::Error e) {
		
	}
}


Napi::Value DWrap::getCfg(const Napi::CallbackInfo& info) {
	Napi::Env env = info.Env();
	Napi::HandleScope scope(env);	

	std::string cfgFile = this->_dnet->getCfg();
	return Napi::String::New(env, cfgFile);
}

Napi::Value DWrap::getX(const Napi::CallbackInfo& info) {
	Napi::Env env = info.Env();
	Napi::HandleScope scope(env);

	int xVal = this->_dnet->x;

	return Napi::Number::New(env, xVal);

}

Napi::Value DWrap::getY(const Napi::CallbackInfo& info) {
	Napi::Env env = info.Env();
	Napi::HandleScope scope(env);

	int yVal = this->_dnet->y;

	return Napi::Number::New(env, yVal);

}

void DWrap::detect(const Napi::CallbackInfo& info) {
	Napi::Env env = info.Env();
	Napi::HandleScope scope(env);

	if (info.Length() < 1) {
		Napi::TypeError::New(env, "Too few arguments.").ThrowAsJavaScriptException();
	}

	Napi::String imgStr = info[0].As<Napi::String>();
	std::string strImg = imgStr.ToString();
	//this->_dnet->initDetect(strImg);

}

DNet* DWrap::GetInternalInstance() {
	return this->_dnet;
}

