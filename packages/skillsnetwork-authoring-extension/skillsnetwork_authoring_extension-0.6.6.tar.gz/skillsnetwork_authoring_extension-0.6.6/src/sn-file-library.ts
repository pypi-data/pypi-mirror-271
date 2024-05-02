import { Widget } from '@lumino/widgets';
import { Dialog } from '@jupyterlab/apputils';

export class SkillsNetworkFileLibraryWidget extends Widget {

  constructor() {

    function constructList(content: string, content_url: string) {
      const list = document.createElement('li');
      const link = document.createElement('a');
      link.textContent = content;
      link.style.color = "brown";
      link.href = content_url;
      link.style.textDecoration = "underline";
      link.style.cursor = "pointer";
      list.appendChild(link);

      return list;
    }

    const container = document.createElement('div');

    const subtitle = document.createElement('h2');
    subtitle.textContent = "File Library is not available for JupyterLab Classic.";
    container.appendChild(subtitle);

    const message = document.createElement('p');
    message.style.textAlign = "left";
    message.textContent = "Try opening the File Library from Author Workbench or upgrade your JupyterLab Classic to JupyterLab Current.";

    const List = document.createElement('ul');
    List.style.textAlign = "left";

    List.appendChild(constructList("How to access File Library from Author Workbench", "https://author.skills.network/docs/labs/jupyterlab-filelibrary"));
    List.appendChild(constructList("How to upgrade to JupyterLab Current", "https://author.skills.network/docs/labs/upgrade-jupyterlab"));

    container.appendChild(message);
    container.appendChild(List);
    container.style.padding = "20px";
    container.style.margin = "10px";
    container.style.textAlign = "center";

    super({ node: container });
  }
}

export class SkillsNetworkFileLibrary {
    launch(){
      const imgLibDialog = new Dialog({title: "Skills Network File Library",
        body:  new SkillsNetworkFileLibraryWidget(),
        hasClose: true,
        buttons: [Dialog.cancelButton()]
      });
      const dialogContent = imgLibDialog.node.querySelector(".jp-Dialog-content")
      if (dialogContent){
        dialogContent.classList.add("sn-file-library-dialog");
      }
      imgLibDialog.launch()
    }
}
