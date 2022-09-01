#pragma once
#include <napi.h>
#include "DNet.h"


class DWrap : public Napi::ObjectWrap<DWrap> {
public:
	static Napi::Object Init(Napi::Env env, Napi::Object exports);
	DWrap(const Napi::CallbackInfo& info);
	DNet* GetInternalInstance();

private:
	static Napi::FunctionReference constructor;
	void loadParams(const Napi::CallbackInfo& info);
	Napi::Value getCfg(const Napi::CallbackInfo& info);
	Napi::Value getX(const Napi::CallbackInfo& info);
	Napi::Value getY(const Napi::CallbackInfo& info);
	void detect(const Napi::CallbackInfo& info);
	DNet* _dnet;
};

