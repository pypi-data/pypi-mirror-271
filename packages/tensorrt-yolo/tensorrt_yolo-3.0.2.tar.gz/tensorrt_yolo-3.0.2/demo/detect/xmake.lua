-- 添加编译规则
add_rules("mode.debug", "mode.release")
set_allowedplats("windows", "linux")
add_requires("opencv", "cli11")
if is_host("linux") then 
    add_requires("zlib")
end

-- 定义选项
option("tensorrt")
    set_showmenu(true)
    set_description("TensorRT Path. Example: /usr/local/tensorrt")
    on_check(function (option)
        if not option:enabled() then 
            raise("TensorRT path is not set. Please specify the TensorRT path.")
        end 
    end)

option("deploy")
    set_showmenu(true)
    set_description("TensorRT-YOLO Project Path.")
    on_check(function (option)
        if not option:enabled() then 
            raise("TensorRT-YOLO project path is not set. Please specify the TensorRT-YOLO Project path.")
        end 
    end)

-- 定义目标
target("detect")
    set_languages("cxx17")
    set_rundir("$(projectdir)")
    add_packages("opencv", "cli11")
    if is_host("linux") then 
        add_packages("zlib")
    end

    -- 添加文件
    add_files("detect.cpp")

    -- 设置目标类型
    set_kind("binary")

    -- 添加 cuda
    add_rules("cuda")
    add_cugencodes("native")

    -- 添加deploy链接目录和链接库
    if has_config("deploy") then
        add_includedirs(path.join("$(deploy)", "include"))
        add_linkdirs(path.join("$(deploy)", "lib"))
        add_links("deploy")

        -- 复制deploy库文件到项目目录
        after_build(function (target)

            -- 定义deploy库文件路径
            local deploy_lib_name = is_host("windows") and "deploy.dll" or "libdeploy.so"
            local deploy_lib_path = path.join("$(deploy)", "lib", deploy_lib_name)

            if os.isfile(deploy_lib_path) then

                -- 目标文件路径
                local deploy_lib_target_path = path.join(target:targetdir(), deploy_lib_name)
            
                -- 复制文件
                os.cp(deploy_lib_path, deploy_lib_target_path)
            end
        end)
    end

    -- 添加TensorRT链接目录和链接库
    if has_config("tensorrt") then
        add_includedirs(path.join("$(tensorrt)", "include"))
        add_linkdirs(path.join("$(tensorrt)", "lib"))
        add_links("nvinfer", "nvinfer_plugin", "nvparsers", "nvonnxparser")
    end