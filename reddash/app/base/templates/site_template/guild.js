// {% if data['status'] == 1 and data['data']['status'] == 1 %}

// {% if 'aliascc' in data['data']['permslist'] and false %}
/* ---------------------------------------------------------------------------------------------------------------------
Aliases group
--------------------------------------------------------------------------------------------------------------------- */

// Alias modal
$(document).on('click', '.editaliasbutton', function () {
    var command = $(this).parent().parent().data("command")
    var textarea = $("#aliasModalCommand")
    textarea.text(command)
    textarea.height(textarea.prop('scrollHeight'))
    $("#aliasModal").modal('toggle')
})

// Fetch aliases
$("#aliases-tab").click(function () {
    $("#fetchaliasesstatus").html("{{ _('Loading...') }}")

    var parts = window.location.pathname.split("/")
    var id = parts[parts.length - 1]
    var xhr = new XMLHttpRequest();
    var url = `{{ url_for('api_blueprint.fetchaliases', guild='00000') }}`.replace("00000", id)

    xhr.open("GET", url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) { return }
        var json = JSON.parse(xhr.responseText)
        if (json.status === 0) {
            $("#fetchaliasesstatus").html(`{{ _('Failed to fetch rules') }}: ${json.message}`)
        } else if (json.status === 1 && json.data.status === 0) {
            $("#fetchaliasesstatus").html(`{{ _('Failed to fetch rules') }}: ${json.data.message}`)
        } else {
            $("#aliasdiv").html("")
            var inside = ""
            for (let [command, aliases] of Object.entries(json.data)) {
                inside += `
                        <tr data-command="${safe(command)}" data-command-aliases="${safe(aliases.raw.join(" "))}">
                            <th><code><span class="prefix">{{ data['data']['prefixes'][0] }}</span>${safe(aliases.shortened)}</code></th>
                            <th>${aliases.humanized}</th>
                            <td>
                                <span class="clickable editaliasbutton">
                                    <i class="tim-icons icon-pencil"></i>
                                </span>
                            </td>
                        </tr>
                    `
            }
            var complete = "{{ _('No aliases are registered on this server') }}"
            if (inside) {
                complete = `
                        <table class="table tablesorter">
                            <thead class="text-primary">
                                <tr>
                                    <th>{{ _('Command') }}</th>
                                    <th>{{ _('Aliases') }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${inside}
                            </tbody>
                        </table>
                    `
            }
            $("#aliasdiv").html(complete)
            $("#fetchaliasesstatus").html("{{ _('Refreshed aliases.') }}")
        }
    }
    try {
        xhr.send()
    } catch (error) {
        console.log(error)
    }
})
// {% endif %}

// {% if 'permissions' in data['data']['permslist'] %}
/* ---------------------------------------------------------------------------------------------------------------------
Permissions group
--------------------------------------------------------------------------------------------------------------------- */

// Add Default Server Rule
$("#adddefaultrulesubmit").click(function () {
    $("#adddefaultrulestatus").html("{{ _('Loading...') }}")
    var allow_or_deny = $("#adddefaultruleallowdeny").val()
    var cog_or_command = $("#adddefaultrulecogcommands").val()

    var parts = window.location.pathname.split("/")
    var id = parts[parts.length - 1]
    var xhr = new XMLHttpRequest();
    var url = `{{ url_for('api_blueprint.adddefaultrule', guild='00000') }}`.replace("00000", id)

    xhr.open("POST", url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) { return }
        var json = JSON.parse(xhr.responseText)
        if (json.status === 0) {
            $("#adddefaultrulestatus").html(`{{ _('Failed to add rule') }}: ${json.message}`)
        } else if (json.status === 1 && json.data.status === 0) {
            $("#adddefaultrulestatus").html(`{{ _('Failed to add rule') }}: ${json.data.message}`)
        } else {
            $("#adddefaultrulestatus").html("{{ _('Rule successfully added') }}.")
        }
    }
    var data = {
        ad: allow_or_deny,
        cc: cog_or_command
    }
    if (data.id == undefined || data.cc == undefined) {
        $("#adddefaultrulestatus").html(`{{ _('Failed to change rule: You must fill out every field.') }}`);
        return
    }
    try {
        xhr.send(JSON.stringify(data))
    } catch (error) {
        console.log(error)
    }
})

// Add Server Rule
$("#addrulesubmit").click(function () {
    $("#addrulestatus").html("{{ _('Loading...') }}")
    var allow_or_deny = $("#addruleallowdeny").val()
    var who_or_what = $("#addruletargets").val()
    var cog_or_command = $("#addrulecogcommands").val()

    var parts = window.location.pathname.split("/")
    var id = parts[parts.length - 1]
    var xhr = new XMLHttpRequest();
    var url = `{{ url_for('api_blueprint.addrule', guild='00000') }}`.replace("00000", id)

    xhr.open("POST", url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) { return }
        var json = JSON.parse(xhr.responseText)
        if (json.status === 0) {
            $("#addrulestatus").html(`{{ _('Failed to add rule') }}: ${json.message}`)
        } else if (json.status === 1 && json.data.status === 0) {
            $("#addrulestatus").html(`{{ _('Failed to add rule') }}: ${json.data.message}`)
        } else {
            $("#addrulestatus").html("{{ _('Rule successfully added') }}.")
        }
    }
    var data = {
        ad: allow_or_deny,
        ww: who_or_what,
        cc: cog_or_command
    }
    if (data.id == undefined || data.cc == undefined || data.ww == undefined) {
        $("#addrulestatus").html(`{{ _('Failed to change rule: You must fill out every field.') }}`);
        return
    }
    try {
        xhr.send(JSON.stringify(data))
    } catch (error) {
        console.log(error)
    }
})

// Remove Default Server Rule
$("#removedefaultrulesubmit").click(function () {
    $("#removedefaultrulestatus").html("{{ _('Loading...') }}")
    var cog_or_command = $("#removedefaultrulecogcommands").val()

    var parts = window.location.pathname.split("/")
    var id = parts[parts.length - 1]
    var xhr = new XMLHttpRequest();
    var url = `{{ url_for('api_blueprint.removedefaultrule', guild='00000') }}`.replace("00000", id)

    xhr.open("POST", url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) { return }
        var json = JSON.parse(xhr.responseText)
        if (json.status === 0) {
            $("#removedefaultrulestatus").html(`{{ _('Failed to remove rule') }}: ${json.message}`)
        } else if (json.status === 1 && json.data.status === 0) {
            $("#removedefaultrulestatus").html(`{{ _('Failed to remove rule') }}: ${json.data.message}`)
        } else {
            $("#removedefaultrulestatus").html("{{ _('Rule successfully removed') }}.")
        }
    }
    var data = {
        cc: cog_or_command
    }
    if (data.cc == undefined) {
        $("#removedefaultrulestatus").html(`{{ _('Failed to change rule: You must fill out every field.') }}`);
        return
    }
    try {
        xhr.send(JSON.stringify(data))
    } catch (error) {
        console.log(error)
    }
})

// Remove Server Rule
$("#removerulesubmit").click(function () {
    $("#removerulestatus").html("{{ _('Loading...') }}")
    var who_or_what = $("#removeruletargets").val()
    var cog_or_command = $("#removerulecogcommands").val()

    var parts = window.location.pathname.split("/")
    var id = parts[parts.length - 1]
    var xhr = new XMLHttpRequest();
    var url = `{{ url_for('api_blueprint.removerule', guild='00000') }}`.replace("00000", id)

    xhr.open("POST", url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) { return }
        var json = JSON.parse(xhr.responseText)
        if (json.status === 0) {
            $("#removerulestatus").html(`{{ _('Failed to remove rule') }}: ${json.message}`)
        } else if (json.status === 1 && json.data.status === 0) {
            $("#removerulestatus").html(`{{ _('Failed to remove rule') }}: ${json.data.message}`)
        } else {
            $("#removerulestatus").html("{{ _('Rule successfully removed') }}.")
        }
    }
    var data = {
        ww: who_or_what,
        cc: cog_or_command
    }
    if (data.cc == undefined || data.ww == undefined) {
        $("#removerulestatus").html(`{{ _('Failed to change rule: You must fill out every field.') }}`);
        return
    }
    try {
        xhr.send(JSON.stringify(data))
    } catch (error) {
        console.log(error)
    }
})

// Fetch users/roles/channels
$(document).ready(function () {
    var select = $(".ruletargets")
    select.selectpicker({ title: "{{ _('Loading...') }}" })
    select.attr("disabled", true)
    select.selectpicker("refresh")

    var parts = window.location.pathname.split("/")
    var id = parts[parts.length - 1]
    var xhr = new XMLHttpRequest();
    var url = `{{ url_for('api_blueprint.fetchtargets', guild='00000') }}`.replace("00000", id)

    xhr.open("GET", url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) { return }

        var json = JSON.parse(xhr.responseText)

        if (json.status === 0) {
            $("#targetstatus").html(`{{ _('Failed to fetch targets') }}: ${json.message}`)
        } else if (json.status === 1 && json.data.status === 0) {
            $("#targetstatus").html(`{{ _('Failed to fetch targets') }}: ${json.data.message}`)
        } else {
            let big_ol_dict = {}
            select.html("")

            var chopt = [`<optgroup label="{{ _('Channels') }}">`]
            for (let [id, name] of json.data.CHANNELS) {
                chopt.push(`<option value=${id} class="selectpicker-element-${id}">${name}</option>`)
                big_ol_dict[id] = name
            }
            chopt.push("</optgroup>")
            select.append(chopt.join(""))

            var ropt = [`<optgroup label="{{ _('Roles') }}">`]
            for (let [id, name] of json.data.ROLES) {
                ropt.push(`<option value=${id} class="selectpicker-element-${id}">${name}</option>`)
                big_ol_dict[id] = name
            }
            ropt.push("</optgroup>")
            select.append(ropt.join(""))

            var uopt = [`<optgroup label="{{ _('Users') }}">`]
            for (let [id, name] of json.data.USERS) {
                uopt.push(`<option value=${id} class="selectpicker-element-${id}">${name}</option>`)
                big_ol_dict[id] = name
            }
            uopt.push("</optgroup>")
            select.append(uopt.join(""))
            /*
            for (let [id, name] of Object.entries(big_ol_dict)) {
    $(`.selectpicker-element-${id}`).text(name)
}
*/
        }
        select.selectpicker({ title: "{{ _('Choose target') }}" })
        select.removeAttr("disabled")
        select.selectpicker("refresh")
    }
    try {
        xhr.send()
    } catch (error) {
        console.log(error)
        select.selectpicker({ title: "{{ _('Choose target') }}" })
        select.removeAttr("disabled")
        select.selectpicker("refresh")
    }
})

// Fetch cogs/commands
$(document).ready(function () {
    var select = $(".cogcommands")
    select.selectpicker({ title: "{{ _('Loading...') }}" })
    select.attr("disabled", true)
    select.selectpicker("refresh")

    var parts = window.location.pathname.split("/")
    var id = parts[parts.length - 1]
    var xhr = new XMLHttpRequest();
    var url = `{{ url_for('api_blueprint.fetchcogcommands', guild='00000') }}`.replace("00000", id)

    xhr.open("GET", url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) { return }

        var json = JSON.parse(xhr.responseText)

        if (json.status === 0) {
            $("#cogcommandstatus").html(`{{ _('Failed to fetch commands') }}: ${json.message}`)
        } else if (json.status === 1 && json.data.status === 0) {
            $("#cogcommandstatus").html(`{{ _('Failed to fetch commands') }}: ${json.data.message}`)
        } else {
            select.html("")

            var copt = [`<optgroup label="{{ _('Cogs') }}">`]
            for (let name of json.data.COGS) {
                copt.push(`<option value="${name}">${name}</option>`)
            }
            copt.push("</optgroup>")
            select.append(copt.join(""))

            var cmopt = [`<optgroup label="{{ _('Commands') }}">`]
            for (let name of json.data.COMMANDS) {
                cmopt.push(`<option value="${name}">${name}</option>`)
            }
            cmopt.push("</optgroup>")
            select.append(cmopt.join(""))
        }
        select.selectpicker({ title: "{{ _('Choose target') }}" })
        select.removeAttr("disabled")
        select.selectpicker("refresh")
    }
    try {
        xhr.send()
    } catch (error) {
        console.log(error)
        select.selectpicker({ title: "{{ _('Choose target') }}" })
        select.removeAttr("disabled")
        select.selectpicker("refresh")
    }
})

// Fetch rules
$("#viewrules-tab").click(function () {
    $("#fetchrulesstatus").html("{{ _('Loading...') }}")
    var parts = window.location.pathname.split("/")

    var id = parts[parts.length - 1]
    var xhr = new XMLHttpRequest();
    var url = `{{ url_for('api_blueprint.fetchrules', guild='00000') }}`.replace("00000", id)

    xhr.open("GET", url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) { return }
        var json = JSON.parse(xhr.responseText)
        if (json.status === 0) {
            $("#fetchrulesstatus").html(`{{ _('Failed to fetch rules') }}: ${json.message}`)
        } else if (json.status === 1 && json.data.status === 0) {
            $("#fetchrulesstatus").html(`{{ _('Failed to fetch rules') }}: ${json.data.message}`)
        } else {
            $("#rulesdiv").html("")
            var overall = ['<h3 style="margin-bottom: 10px">{{ _("Cog rules") }}</h3>']
            var allcoglines = ["<ul>"]

            let big_ol_dict_two = {}
            let cog_counter = 0

            for (let [cog, rules] of Object.entries(json.data.COG)) {
                var coglines = []
                for (let rule of rules) {
                    if (rule.type === "Default") {
                        coglines.unshift(`<li>{{ _('By default, users are') }} ${rule.permission} {{ _('permission to use the') }} <code>${cog}</code> {{ _('cog') }}.</li>`)
                    } else if (rule.type === "Role") {
                        coglines.push(`<li>{{ _('Users with the') }} <code id="cog-rules-${cog_counter}">Loading...</code> {{ _('role') }} (${rule.id}) {{ _('are') }} ${rule.permission} {{ _('permission to use the') }} <code>${cog}</code> {{ _('cog') }}.</li>`)
                    } else if (rule.type === "Channel") {
                        coglines.push(`<li>{{ _('Users in the') }} <code id="cog-rules-${cog_counter}">Loading...</code> {{ _('channel') }} (${rule.id}) {{ _('are') }} ${rule.permission} {{ _('permission to use the') }} <code>${cog}</code> {{ _('cog') }}.</li>`)
                    } else {
                        coglines.push(`<li>{{ _('User') }} <code id="cog-rules-${cog_counter}">Loading...</code> (${rule.id}) {{ _('is') }} ${rule.permission} {{ _('permission to use the') }} <code>${cog}</code> {{ _('cog') }}.</li>`)
                    }
                    big_ol_dict_two[`cog-rules-${cog_counter}`] = rule.name
                    cog_counter += 1
                }
                if (coglines) {
                    allcoglines = allcoglines.concat(coglines)
                }
            }
            allcoglines.push("</ul>")
            if (allcoglines.length == 2) {
                allcoglines = ["<p>{{ _('No cog rules have been created') }}.</p>"]
            }
            overall = overall.concat(allcoglines)

            overall.push('<h3 style="margin-bottom: 10px">{{ _("Command rules") }}</h3>')
            var allcmdlines = ["<ul>"]

            let cmd_counter = 0

            for (let [cmd, rules] of Object.entries(json.data.COMMAND)) {
                var cmdlines = []
                for (let rule of rules) {
                    if (rule.type === "Default") {
                        cmdlines.unshift(`<li>{{ _('By default, users are') }} ${rule.permission} {{ _('permission to use the') }} <code>${cmd}</code> {{ _('command') }}.</li>`)
                    } else if (rule.type === "Role") {
                        cmdlines.push(`<li>{{ _('Users with the') }} <code id="cmd-rules-${cmd_counter}">Loading...</code> {{ _('role') }} (${rule.id}) {{ _('are') }} ${rule.permission} {{ _('permission to use the') }} <code>${cmd}</code> {{ _('command') }}.</li>`)
                    } else if (rule.type === "Channel") {
                        cmdlines.push(`<li>{{ _('Users in the') }} <code id="cmd-rules-${cmd_counter}">Loading...</code> {{ _('channel') }} (${rule.id}) {{ _('are') }} ${rule.permission} {{ _('permission to use the') }} <code>${cmd}</code> {{ _('command') }}.</li>`)
                    } else {
                        cmdlines.push(`<li>{{ _('User') }} <code id="cmd-rules-${cmd_counter}">Loading...</code> (${rule.id}) {{ _('is') }} ${rule.permission} {{ _('permission to use the') }} <code>${cmd}</code> {{ _('command') }}.</li>`)
                    }
                    big_ol_dict_two[`cmd-rules-${cmd_counter}`] = rule.name
                    cmd_counter += 1
                }
                if (cmdlines) {
                    allcmdlines = allcmdlines.concat(cmdlines)
                }
            }
            allcmdlines.push("</ul>")
            if (allcmdlines.length === 2) {
                allcmdlines = ["<p>{{ _('No command rules have been created') }}.</p>"]
            }
            overall = overall.concat(allcmdlines)
            $("#rulesdiv").html(overall.join(""))
            for (let [id, name] of Object.entries(big_ol_dict_two)) {
                $(`#${id}`).text(name)
            }
            $("#fetchrulesstatus").html("{{ _('Refreshed rules') }}.")
        }
    }
    try {
        xhr.send()
    } catch (error) {
        console.log(error)
    }
})
// {% endif %}

// {% if 'botsettings' in data['data']['permslist'] %}
/* ---------------------------------------------------------------------------------------------------------------------
Bot settings group
--------------------------------------------------------------------------------------------------------------------- */
// Admin role controls
$(document).on('click', '.admin-role-x', function () {
    var input = $(this).parent().siblings().first().children().first()
    $(".adminroleoption").parent().append(`
    <a class="dropdown-item clickable adminroleoption" data-id="${input.attr(" data-id")}">${input.val()}</a>
`)
    var li = $(this).parent().parent().parent()
    li.fadeOut(complete = function () {
        li.remove()
    })
})

$(document).on('click', '.adminroleoption', function () {
    var elm = $(this)
    let random_number = Math.floor(Math.random() * Math.floor(100000))
    $("#adminrolelist").append(`
    < li >
    <div class="row">
        <div class="col-md-10 col-8">
            <input class="form-control adminroleinput" value="Loading..." disabled=True data-id="${elm.attr(" data-id")}" id="admin-role-${random_number}">
        </div>
        <div class="col-md-1 col-1">
            <span class="admin-role-x clickable"><i class="tim-icons icon-simple-remove" style="float: right; margin-top: 10px;"></i></span>
        </div>
    </div>
                </li >
    `)
    $(`#admin - role - ${random_number} `).val(elm.text())
    elm.remove()
})

$("#adminroleupdate").click(function () {
    $("#adminrolestatus").html("{{ _('Loading...') }}")
    var roles = []
    $(".adminroleinput").each(function (index, elm) {
        roles.push($(elm).attr("data-id"))
    })

    var parts = window.location.pathname.split("/")
    var id = parts[parts.length - 1]
    var xhr = new XMLHttpRequest();
    var url = `{ { url_for('api_blueprint.adminroles', guild = '00000') } } `.replace("00000", id)

    xhr.open("POST", url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) { return }
        var json = JSON.parse(xhr.responseText)
        if (json.status === 0) {
            $("#adminrolestatus").html(`{ { _('Failed to update admin roles') } }: ${json.message} `)
        } else if (json.status === 1 && json.data.status === 0) {
            $("#adminrolestatus").html(`{ { _('Failed to update admin roles') } }: ${json.data.message} `)
        } else {
            $("#adminrolestatus").html("{{ _('Admin roles successfully updated') }}.")
        }
    }
    var data = {
        "roles": roles
    }
    try {
        xhr.send(JSON.stringify(data))
    } catch (error) {
        console.log(error)
    }
})

// Mod role controls
$(document).on('click', '.mod-role-x', function () {
    var input = $(this).parent().siblings().first().children().first()
    $(".modroleoption").parent().append(`
    < a class="dropdown-item clickable modroleoption" data - id="${input.attr("data - id")}" > ${input.val()}</a >
        `)
    var li = $(this).parent().parent().parent()
    li.fadeOut(complete = function () {
        li.remove()
    })
})

$(document).on('click', '.modroleoption', function () {
    var elm = $(this)
    let random_number = Math.floor(Math.random() * Math.floor(100000))
    $("#modrolelist").append(`
        < li >
        <div class="row">
            <div class="col-md-10 col-8">
                <input class="form-control modroleinput" value="Loading..." disabled=True data-id="${elm.attr(" data-id")}" id="mod-role-${random_number}">
            </div>
            <div class="col-md-1 col-1">
                <span class="mod-role-x clickable"><i class="tim-icons icon-simple-remove" style="float: right; margin-top: 10px;"></i></span>
            </div>
        </div>
                </li >
    `)
    $(`#mod - role - ${random_number} `).val(elm.text())
    elm.remove()
})

$("#modroleupdate").click(function () {
    $("#modrolestatus").html("{{ _('Loading...') }}")
    var roles = []
    $(".modroleinput").each(function (index, elm) {
        roles.push($(elm).attr("data-id"))
    })

    var parts = window.location.pathname.split("/")
    var id = parts[parts.length - 1]
    var xhr = new XMLHttpRequest();
    var url = `{ { url_for('api_blueprint.modroles', guild = '00000') } } `.replace("00000", id)

    xhr.open("POST", url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) { return }
        var json = JSON.parse(xhr.responseText)
        if (json.status === 0) {
            $("#modrolestatus").html(`{ { _('Failed to update mod roles') } }: ${json.message} `)
        } else if (json.status === 1 && json.data.status === 0) {
            $("#modrolestatus").html(`{ { _('Failed to update mod roles') } }: ${json.data.message} `)
        } else {
            $("#modrolestatus").html("{{ _('Mod roles successfully updated.') }}")
        }
    }
    var data = {
        "roles": roles
    }
    try {
        xhr.send(JSON.stringify(data))
    } catch (error) {
        console.log(error)
    }
})

// Prefix Controls
$(document).on('click', '.prefix-x', function () {
    var li = $(this).parent().parent().parent()
    li.fadeOut(complete = function () {
        li.remove()
    })
})
$("#addprefix").click(function () {
    $("#prefixlist").append(`
    < li >
    <div class="row">
        <div class="col-md-10 col-8">
            <input class="form-control prefixinput">
        </div>
        <div class="col-md-1 col-1">
            <span class="prefix-x clickable"><i class="tim-icons icon-simple-remove" style="float: right; margin-top: 10px;"></i></span>
        </div>
    </div>
                </li >
    `)
})
$("#prefixupdate").click(function () {
    $("#prefixstatus").html("{{ _('Loading...') }}")
    var prefixes = []
    $(".prefixinput").each(function (index, elm) {
        var text = $(elm).val()
        if (text) {
            prefixes.push(text)
        }
    })

    var parts = window.location.pathname.split("/")
    var id = parts[parts.length - 1]
    var xhr = new XMLHttpRequest();
    var url = `{ { url_for('api_blueprint.serverprefix', guild = '00000') } } `.replace("00000", id)

    xhr.open("POST", url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) { return }
        var json = JSON.parse(xhr.responseText)
        if (json.status === 0) {
            $("#prefixstatus").html(`{ { _('Failed to update prefixes') } }: ${json.message} `)
        } else if (json.status === 1 && json.data.status === 0) {
            $("#prefixstatus").html(`{ { _('Failed to update prefixes') } }: ${json.data.message} `)
        } else {
            $("#prefixstatus").html("{{ _('Prefixes successfully updated') }}.")
        }
    }
    var data = {
        "prefixes": prefixes
    }
    try {
        xhr.send(JSON.stringify(data))
    } catch (error) {
        console.log(error)
    }
})
// {% endif %}

// {% endif %}